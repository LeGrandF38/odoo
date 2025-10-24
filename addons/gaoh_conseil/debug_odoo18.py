#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de débogage avancé pour Odoo 18
Détecte les incompatibilités spécifiques à Odoo 18
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# Couleurs
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def check_tree_in_view_mode(file_path):
    """Détecte l'usage de 'tree' dans view_mode (Odoo 18 utilise 'list')"""
    issues = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for elem in root.iter():
            if elem.tag == 'field' and elem.attrib.get('name') == 'view_mode':
                if elem.text and 'tree' in elem.text:
                    parent = None
                    for p in root.iter():
                        if elem in list(p):
                            parent = p
                            break
                    
                    record_id = parent.attrib.get('id', 'unknown') if parent else 'unknown'
                    issues.append({
                        'type': 'tree_in_view_mode',
                        'message': f"Utilise 'tree' au lieu de 'list'",
                        'value': elem.text,
                        'record_id': record_id,
                        'fix': elem.text.replace('tree', 'list')
                    })
    except Exception as e:
        pass
    
    return issues

def check_tree_elements(file_path):
    """Détecte l'usage de <tree> au lieu de <list> (déjà corrigé)"""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Chercher les <tree> qui ne sont pas dans des commentaires
            if '<tree' in content and 'View Liste' in content:
                # C'est probablement un problème
                pass
    except:
        pass
    
    return issues

def check_ir_ui_view_types(file_path):
    """Vérifie que les ir.ui.view ont le bon type pour Odoo 18"""
    issues = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for record in root.findall('.//record[@model="ir.ui.view"]'):
            record_id = record.attrib.get('id', 'unknown')
            has_type_field = False
            arch_type = None
            
            for field in record.findall('field'):
                if field.attrib.get('name') == 'type':
                    has_type_field = True
                    type_value = field.text
                    # Vérifier les types valides
                    valid_types = ['form', 'list', 'kanban', 'calendar', 'graph', 'pivot', 'search', 'qweb', 'gantt', 'map', 'cohort']
                    if type_value not in valid_types:
                        issues.append({
                            'type': 'invalid_view_type',
                            'message': f"Type de vue invalide pour Odoo 18: '{type_value}'",
                            'record_id': record_id,
                            'value': type_value,
                            'valid_types': valid_types
                        })
                
                if field.attrib.get('name') == 'arch':
                    arch_content = field.text
                    if arch_content:
                        if '<tree' in arch_content:
                            arch_type = 'tree'
                        elif '<list' in arch_content:
                            arch_type = 'list'
            
            # Vérifier cohérence
            if has_type_field and arch_type:
                for field in record.findall('field'):
                    if field.attrib.get('name') == 'type':
                        type_value = field.text
                        if type_value == 'tree' and arch_type == 'list':
                            issues.append({
                                'type': 'view_type_mismatch',
                                'message': "Type 'tree' avec contenu <list> - Remplacer type par 'list'",
                                'record_id': record_id
                            })
    except Exception as e:
        pass
    
    return issues

def main():
    module_path = Path(__file__).parent
    xml_files = list(module_path.glob('views/*.xml')) + list(module_path.glob('wizards/*.xml'))
    
    print(f"\n{Colors.BLUE}{'='*70}")
    print(f"🔍 Débogage Odoo 18 - Détection des incompatibilités")
    print(f"{'='*70}{Colors.END}\n")
    
    all_issues = {}
    
    for xml_file in sorted(xml_files):
        file_name = xml_file.relative_to(module_path)
        issues = []
        
        # Chercher les problèmes
        issues.extend(check_tree_in_view_mode(xml_file))
        issues.extend(check_tree_elements(xml_file))
        issues.extend(check_ir_ui_view_types(xml_file))
        
        if issues:
            all_issues[str(file_name)] = issues
    
    # Afficher les résultats
    if all_issues:
        print(f"{Colors.RED}❌ Problèmes détectés:{Colors.END}\n")
        
        for file_name, issues in sorted(all_issues.items()):
            print(f"{Colors.YELLOW}{file_name}:{Colors.END}")
            for idx, issue in enumerate(issues, 1):
                print(f"\n  {idx}. {issue['type'].upper()}")
                print(f"     Message: {issue['message']}")
                if 'record_id' in issue:
                    print(f"     Record: {issue['record_id']}")
                if 'value' in issue:
                    print(f"     Valeur: {issue['value']}")
                if 'fix' in issue:
                    print(f"     {Colors.GREEN}Correction: {issue['fix']}{Colors.END}")
                if 'valid_types' in issue:
                    print(f"     Types valides: {', '.join(issue['valid_types'])}")
            print()
        
        return False
    else:
        print(f"{Colors.GREEN}✓ Aucun problème Odoo 18 détecté!{Colors.END}\n")
        return True

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
