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
    """Parse genérico para arquivos .md de profiling, adaptando-se ao conteúdo."""
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

def parse_pipeline_quality_log(content):
    """Parse de logs de qualidade de pipeline."""
    data = {"report_type": "Pipeline Quality", "tests": []}
    
    title_match = re.search(r'REPORT\s*-\s*(.*?)(?:\s*\|\s*RUN:\s*(\d+))?', content, re.IGNORECASE)
    if title_match:
        data['title'] = title_match.group(1).strip()
        data['run_id'] = title_match.group(2) if title_match.group(2) else ""

    lines = content.split('\n')
    for line in lines:
        if '|' in line and '---' not in line:
            parts = [x.strip() for x in line.split('|') if x.strip()]
            if len(parts) >= 3 and "TESTE" not in parts[0].upper():
                data['tests'].append({
                    "test": parts[0],
                    "status": parts[1],
                    "obs": parts[2]
                })
    
    res = re.search(r'Resultado Final:\s*(\w+)', content, re.IGNORECASE)
    if res: 
        data['final_result'] = res.group(1).upper()
        
    return data

def parse_abt_technical_report(content):
    """Parse de logs técnicos de ABT (Gold)."""
    data = {"report_type": "Pipeline Quality", "tests": []} 
    
    title_match = re.search(r'RELATÓRIO TÉCNICO ABT - (.*?) \| RUN: (\d+)', content)
    if title_match:
        data['title'] = title_match.group(1).strip()
        data['run_id'] = title_match.group(2)

    metrics = re.findall(r'(?:.)?\s*(.*?):\s*(.*)', content)
    
    for metric_name, value in metrics:
        name = metric_name.strip()
        if name and name != "Status":
            data['tests'].append({
                "test": name,
                "status": "INFO",
                "obs": value.strip()
            })
    
    status_match = re.search(r'Status:\s*(.*)', content)
    if status_match:
        status_text = status_match.group(1).strip()
        data['final_result'] = "SUCCESS" if "Sucesso" in status_text else "FAILED"
        data['tests'].insert(0, {"test": "Status Geral", "status": "✅" if "Sucesso" in status_text else "❌", "obs": status_text})

    return data

def parse_pipeline_execution_log(content):
    """Parse de logs de execução global do pipeline (DATA PIPELINE EXECUTION)."""
    data = {
        "report_type": "Pipeline Execution",
        "steps": []
    }
    
    run_id = re.search(r'RUN_ID:\s+(\d+)', content)
    operador = re.search(r'OPERADOR:\s+(\w+)', content)
    timestamp = re.search(r'^([\d\- :]+) \| \[START\]', content, re.MULTILINE)
    tempo_total = re.search(r'TEMPO TOTAL:\s+([\d:]+)', content)
    
    if run_id: data['run_id'] = run_id.group(1)
    if operador: data['operador'] = operador.group(1)
    if timestamp: data['timestamp'] = timestamp.group(1)
    if tempo_total: data['tempo_total'] = tempo_total.group(1)

    step_matches = re.findall(r'([\d\- :]+) \| \[SUCCESS\]\s*\| (.*?) \s*\| Status: (.*?) \| Duração: ([\d:]+)', content)
    
    for match in step_matches:
        data['steps'].append({
            "timestamp": match[0],
            "step": match[1].strip(),
            "status": match[2].strip(),
            "duration": match[3].strip()
        })
        
    return data

def main():
    base_dir = "reports"
    for root, _, files in os.walk(base_dir):
        for file in files:
            path = os.path.join(root, file)
            try:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.rar', '.zip', '.json')):
                    continue

                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content_upper = content.upper()
                parsed = None

                if file.endswith('.md'):
                    parsed = parse_profiling_md(content, path)
                
                elif file.endswith('.log'):
                    if "DATA PIPELINE EXECUTION" in content_upper:
                        parsed = parse_pipeline_execution_log(content)

                    elif "AUDITORIA DE PARTIÇÕES" in content_upper:
                        parsed = parse_integrity_log(content)
                    
                    elif "DATA CONTRACT AUDIT" in content_upper:
                        parsed = parse_pandera_log(content)
                    
                    elif "RELATÓRIO TÉCNICO ABT" in content_upper:
                        parsed = parse_abt_technical_report(content)
                    
                    elif "QUALITY REPORT" in content_upper or "REPORT -" in content_upper:
                        parsed = parse_pipeline_quality_log(content)
                
                if parsed:
                    out_path = os.path.splitext(path)[0] + ".json"
                    with open(out_path, 'w', encoding='utf-8') as f:
                        json.dump(parsed, f, indent=4, ensure_ascii=False)
                    print(f"✅ {file} -> JSON")
                else:
                    if file.endswith('.log'):
                        print(f"⚠️ {file} ignorado (padrão de conteúdo não reconhecido)")

            except Exception as e:
                print(f"❌ Erro em {file}: {e}")

if __name__ == "__main__":
    main()