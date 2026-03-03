import os
import json
import re

def md_table_to_dict(table_str):
    """Converte uma tabela markdown em uma lista de dicionários."""
    if not table_str:
        return []
    lines = [line.strip() for line in table_str.strip().split('\n') if line.strip()]
    if len(lines) < 2:
        return []
    
    headers = [h.strip() for h in lines[0].split('|') if h.strip()]
    
    data_start_idx = 1
    if len(lines) > 1 and all(c in '-:| ' for c in lines[1]):
        data_start_idx = 2
        
    data_rows = []
    for line in lines[data_start_idx:]:
        cols = [c.strip() for c in line.split('|') if c.strip()]
        if len(cols) > 0:
            row = {}
            for i, header in enumerate(headers):
                row[header] = cols[i] if i < len(cols) else ""
            data_rows.append(row)
    return data_rows

def parse_profiling_md(content, filepath):
    """Parse genérico para arquivos .md de profiling."""
    data = {
        "report_type": "Profiling",
        "source_file": os.path.basename(filepath),
        "sections": []
    }
    
    title_match = re.search(r'^# (.*)', content)
    if title_match:
        data["title"] = title_match.group(1).strip()

    parts = re.split(r'\n(#{2,4} .*)', content)
    
    current_section = None
    for part in parts:
        part = part.strip()
        if not part: continue
        
        header_match = re.match(r'^(#{2,4}) (.*)', part)
        if header_match:
            current_section = {
                "header": header_match.group(2).strip(),
                "content": []
            }
            data["sections"].append(current_section)
        elif current_section:
            metadata = re.findall(r'- \*\*(.*?)\:\*\* `?(.*?)`?(?:\n|$)', part)
            if metadata:
                current_section["metadata"] = {k.strip(): v.strip() for k, v in metadata}
            
            tables = re.findall(r'(\|[^\n]+\|\n\|[\s\-\:\|]+\|\n(?:\|[^\n]+\|\n?)+)', part)
            for table in tables:
                current_section["content"].append({
                    "type": "table",
                    "data": md_table_to_dict(table)
                })
            
            if not tables and not metadata and len(part) > 10:
                clean_text = re.sub(r'\*+', '', part).strip()
                current_section["content"].append({
                    "type": "text",
                    "data": clean_text
                })

    return data

def parse_integrity_log(content):
    """Parse de logs de auditoria de partições."""
    data = {"report_type": "Partition Audit", "tables": []}
    ts_match = re.search(r'AUDITORIA DE PARTIÇÕES .*? - ([\d\- :]+)', content)
    if ts_match: data['timestamp'] = ts_match.group(1)
        
    table_blocks = re.split(r'📊 TABELA: ', content)[1:]
    for block in table_blocks:
        lines = block.strip().split('\n')
        table_name = lines[0].strip()
        run_id = re.search(r'🆔 Run ID: (\d+)', block)
        col = re.search(r'Coluna: (\w+)', block)
        window = re.search(r'📅 Janela: (.*)', block)
        
        partitions = []
        p_matches = re.findall(r'📁 (\d+): \s*([\d,]+) linhas \| Min: ([\d\- :]+) \| Max: ([\d\- :]+) \| (.*)', block)
        for p in p_matches:
            partitions.append({
                "partition": p[0], "rows": int(p[1].replace(',', '')),
                "min": p[2], "max": p[3], "status": p[4].strip()
            })
        data['tables'].append({
            "table": table_name, "run_id": run_id.group(1) if run_id else "",
            "column": col.group(1) if col else "", "window": window.group(1) if window else "",
            "partitions": partitions
        })
    return data

def parse_quality_bronze_log(content):
    """Parse específico para quality da camada Bronze (dimensões)."""
    TEST_DESCRIPTIONS = {
        "Volumetria Dimensão": "Quantidade de registros existentes na dimensão carregada na camada Bronze.",
        "Chave Técnica": "Identifica qual coluna representa a chave substituta da dimensão no DW.",
        "Match de Tipagem Chave Técnica": "Verifica se o tipo de dado da chave técnica entre fato e dimensão é compatível.",
        "Integridade de Chave (Fato)": "Valida se todos os registros da fato possuem correspondência válida na dimensão."
    }
    data = {"report_type": "Pipeline Quality", "layer": "bronze", "reports": []}
    blocks = re.split(r'📋 QUALITY REPORT - ', content)[1:]
    for block in blocks:
        lines = block.strip().split('\n')
        header_match = re.match(r'(.*?)\s*\|\s*RUN:\s*(\d+)', lines[0])
        if not header_match: continue
        report = {"entity": header_match.group(1).strip(), "run_id": header_match.group(2).strip(), "tests": []}
        for line in lines:
            if '|' not in line or '---' in line or 'TESTE' in line.upper(): continue
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) < 3: continue
            report["tests"].append({
                "test": parts[0], "status": parts[1], "obs": parts[2],
                "description": TEST_DESCRIPTIONS.get(parts[0], "Validação de qualidade Bronze.")
            })
        res = re.search(r'Resultado Final:\s*(\w+)', block)
        report["final_result"] = res.group(1) if res else "UNKNOWN"
        data["reports"].append(report)
    return data

def parse_quality_silver_log(content):
    """Parse atualizado para layout de qualidade da camada Silver com métricas de saneamento."""
    data = {"report_type": "Pipeline Quality", "layer": "silver", "reports": []}
    
    blocks = re.split(r'📋 QUALITY REPORT - ', content)[1:]
    
    for block in blocks:
        lines = block.strip().split('\n')
        header_match = re.match(r'(.*?)\s*\|\s*RUN:\s*(\d+)', lines[0])
        if not header_match: continue
        
        report = {
            "entity": header_match.group(1).strip(),
            "run_id": header_match.group(2).strip(),
            "tests": [],
            "total_added_columns": 0,
            "total_processed_records": 0
        }
        
        for line in lines:
            if '|' not in line or '---' in line or 'PAREAMENTO' in line.upper(): 
                continue
            
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 5: continue
            
            perc_match = re.search(r'\((.*?)\)', parts[2])
            perc_val = perc_match.group(1) if perc_match else "100.0%"
            
            report["tests"].append({
                "pairing": parts[0],
                "status": parts[1],
                "efficiency_score": perc_val,
                "null_values": parts[3],
                "no_match_values": parts[4],
                "description": "Validação de integridade referencial e higienização de nulos."
            })
        
        total_cols_match = re.search(r'Total de Colunas Adicionadas:\s*(\d+)', block)
        if total_cols_match: 
            report["total_added_columns"] = int(total_cols_match.group(1))
            
        total_rec_match = re.search(r'Total de Registros Processados:\s*([\d.]+)', block)
        if total_rec_match:
            report["total_processed_records"] = total_rec_match.group(1)

        report["final_result"] = "SUCCESS" if all(t["status"].upper() in ["PASS", "SUCCESS"] for t in report["tests"]) else "CHECK_REQUIRED"
        
        data["reports"].append(report)
        
    return data

def parse_abt_technical_report(content):
    """Parse robusto para o novo layout tabular de ABT Gold."""
    data = {
        "report_type": "ABT Technical Report", 
        "entity": "N/I",
        "run_id": "N/I",
        "metadata": {},
        "integrity_table": []
    }
    
    # 1. Título e Run ID (Busca por RUN: 2026...)
    title_match = re.search(r'REPORT - (.*?) \| RUN: (\d+)', content)
    if title_match:
        data['entity'] = title_match.group(1).strip()
        data['run_id'] = title_match.group(2)
    
    # 2. Metadados do Cabeçalho - Regex focado nas palavras-chave e números com pontos
    patterns = {
        "status": r'STATUS GERAL:\s*(.*?)\s*\|',
        "variables": r'VARIÁVEIS:\s*(\d+)',
        "volumetry": r'REGISTROS:\s*([\d.]+)',
        "cardinality": r'CPFs ÚNICOS:\s*([\d.]+)'
    }
    
    for key, pattern in patterns.items():
        m = re.search(pattern, content)
        if m: data["metadata"][key] = m.group(1).strip()
    
    data["metadata"]["grain"] = "CPF + SAFRA + PROD"

    # 3. Tabela de Integridade
    # Filtra linhas que possuem o pipe | mas ignora cabeçalhos e divisores
    for line in content.split('\n'):
        if '|' in line and 'FONTE DE DADOS' not in line and '=' not in line and '-' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5:
                data["integrity_table"].append({
                    "source": parts[0],
                    "type": parts[1],
                    "status": parts[2],
                    "coverage": parts[3],
                    "additional_info": parts[4]
                })
                
    return data

def parse_quality_gold_log(content):
    """Parse de logs de qualidade Gold (Labels/Features) - PADRÃO 2."""
    data = {"report_type": "Pipeline Quality", "layer": "gold", "groups": []}
    header_match = re.search(r'📋 QUALITY REPORT - (.*?) \| RUN: (\d+)', content)
    if header_match:
        data["entity"] = header_match.group(1).strip()
        data["run_id"] = header_match.group(2).strip()

    TEST_DESCRIPTIONS = {
        "Unicidade": "Valida unicidade de grão.",
        "Missing": "Valida se a variável target (Label) não possui valores nulos.",
        "Saneamento": "Volume de dados descartados na transição Silver -> Gold.",
        "Safra": "Analisa a representatividade temporal da janela de dados.",
        "Overlap": "Percentual de cobertura de CPFs."
    }

    sections = content.split('----------------------------------------------------------------------------------')
    clean_sections = [s.strip() for s in sections if s.strip() and "TESTE" not in s and "QUALITY REPORT" not in s]

    for idx, section in enumerate(clean_sections):
        group_data = {"group_id": idx + 1, "tests": []}
        if "Unicidade" in section: group_data["group_name"] = "Integridade de Chaves e Target"
        elif "Distribuição Safra" in section: group_data["group_name"] = "Saúde da Janela Temporal"
        elif "Overlap" in section: group_data["group_name"] = "Densidade de Cruzamento (Lineage)"
        elif "Saneamento" in section: group_data["group_name"] = "Resumo de Expurgos"
        else: group_data["group_name"] = f"Métricas Adicionais"

        for line in section.split('\n'):
            if '|' in line:
                p = [x.strip() for x in line.split('|')]
                if len(p) >= 3:
                    desc_key = next((k for k in TEST_DESCRIPTIONS.keys() if k in p[0]), "Validação Gold.")
                    group_data["tests"].append({
                        "test": p[0], "status": p[1], "obs": p[2],
                        "description": TEST_DESCRIPTIONS.get(desc_key)
                    })
        if group_data["tests"]: data["groups"].append(group_data)
    return data

def parse_pandera_log(content):
    """Parse de logs Pandera."""
    data = {"report_type": "Data Contract Audit", "results": []}
    ts = re.search(r'AUDIT \| ([\d\- :]+)', content)
    if ts: data['timestamp'] = ts.group(1)
    for line in content.split('\n'):
        if '|' in line and ('✅' in line or '❌' in line):
            p = [x.strip() for x in line.split('|')]
            if len(p) >= 3: data['results'].append({"status": p[0], "cols": p[1], "detail": p[2]})
    return data

def parse_pipeline_execution_log(content):
    """Parse robusto de logs de execução global do pipeline (somente última execução)."""
    
    data = {
        "report_type": "Pipeline Execution",
        "steps": []
    }


    last_end_index = content.rfind("[END]")

    if last_end_index == -1:
        return data

    start_index = content.rfind("[START]", 0, last_end_index)

    if start_index == -1:
        return data

    last_block = content[start_index:last_end_index]

    run_id = re.search(r'RUN_ID:\s+(\d+)', last_block)
    if run_id:
        data['run_id'] = run_id.group(1)

    steps = re.findall(
        r'([\d\- :]+) \| \[SUCCESS\]\s*\| (.*?) \s*\| Status: (.*?) \| Duração: ([\d:]+)',
        last_block
    )

    seen = set()

    for match in steps:
        step_name = match[1].strip()

        if step_name in seen:
            continue

        seen.add(step_name)

        data['steps'].append({
            "timestamp": match[0],
            "step": step_name,
            "status": match[2].strip(),
            "duration": match[3].strip()
        })

    total_time = re.search(r'TEMPO TOTAL:\s*([\d:]+)', last_block)
    if total_time:
        data['tempo_total'] = total_time.group(1)

    return data

def main():
    base_dir = "reports"
    for root, _, files in os.walk(base_dir):
        for file in files:
            path = os.path.join(root, file)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.rar', '.zip', '.json', '.pkl', '.parquet', '.cbm')): continue
            try:
                with open(path, 'r', encoding='utf-8') as f: content = f.read()
                content_upper = content.upper()
                parsed = None
                if file.endswith('.md'): parsed = parse_profiling_md(content, path)
                elif file.endswith('.log'):
                    if "DATA PIPELINE EXECUTION" in content_upper: parsed = parse_pipeline_execution_log(content)
                    elif "AUDITORIA DE PARTIÇÕES" in content_upper: parsed = parse_integrity_log(content)
                    elif "DATA CONTRACT AUDIT" in content_upper: parsed = parse_pandera_log(content)
                    elif "GOLD ABT REPORT" in content_upper: parsed = parse_abt_technical_report(content)
                    elif "QUALITY REPORT" in content_upper:
                        cp = path.replace("\\", "/")
                        if "pipeline/gold" in cp: parsed = parse_quality_gold_log(content)
                        elif "pipeline/silver" in cp: parsed = parse_quality_silver_log(content)
                        elif "pipeline/bronze" in cp: parsed = parse_quality_bronze_log(content)
                if parsed:
                    with open(os.path.splitext(path)[0] + ".json", 'w', encoding='utf-8') as f:
                        json.dump(parsed, f, indent=4, ensure_ascii=False)
                    print(f"✅ {file} -> JSON")
            except Exception as e: print(f"❌ Erro em {file}: {e}")

if __name__ == "__main__": main()