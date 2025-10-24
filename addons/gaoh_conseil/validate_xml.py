#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation XML pour le module gaoh_conseil
Vérifie que tous les fichiers XML sont bien formés et contiennent les éléments requis.
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def validate_xml_syntax(file_path):
    """Valide la syntaxe XML d'un fichier"""
    try:
        tree = ET.parse(file_path)
        return True, "OK"
    except ET.ParseError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def extract_ids(file_path):
    """Extrait tous les IDs définis dans un fichier XML"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ids = set()
        
        for elem in root.iter():
            if 'id' in elem.attrib:
                ids.add(elem.attrib['id'])
        
        return ids
    except:
        return set()

def extract_references(file_path):
    """Extrait toutes les références à des IDs (action, parent, etc.)"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        refs = set()
        
        for elem in root.iter():
            # Références dans l'attribut 'action'
            if 'action' in elem.attrib:
                action = elem.attrib['action']
                if action and not action.startswith('$'):  # Ignorer les références dynamiques
                    refs.add(('action', action))
            
            # Références dans l'attribut 'parent'
            if 'parent' in elem.attrib:
                parent = elem.attrib['parent']
                if parent:
                    refs.add(('parent', parent))
            
            # Références dans les éléments de texte
            if elem.tag == 'field' and elem.attrib.get('name') == 'ref':
                if elem.text:
                    refs.add(('field_ref', elem.text))
        
        return refs
    except:
        return set()

def main():
    module_path = Path(__file__).parent
    xml_files = list(module_path.glob('views/*.xml')) + list(module_path.glob('wizards/*.xml'))
    
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"Validation du module gaoh_conseil")
    print(f"{'='*60}{Colors.END}\n")
    
    # Étape 1: Validation syntaxe XML
    print(f"{Colors.BLUE}1. Validation de la syntaxe XML{Colors.END}")
    print(f"{'-'*60}")
    
    all_valid = True
    all_ids = {}
    all_refs = {}
    
    for xml_file in sorted(xml_files):
        is_valid, msg = validate_xml_syntax(xml_file)
        file_name = xml_file.relative_to(module_path)
        
        if is_valid:
            print(f"{Colors.GREEN}✓ {file_name}{Colors.END}")
            ids = extract_ids(xml_file)
            refs = extract_references(xml_file)
            all_ids[str(file_name)] = ids
            all_refs[str(file_name)] = refs
        else:
            print(f"{Colors.RED}✗ {file_name}{Colors.END}")
            print(f"  Erreur: {msg}")
            all_valid = False
    
    if not all_valid:
        print(f"\n{Colors.RED}❌ Erreurs XML détectées!{Colors.END}\n")
        return False
    
    print(f"\n{Colors.GREEN}✓ Tous les fichiers XML sont valides{Colors.END}\n")
    
    # Étape 2: Validation des références
    print(f"{Colors.BLUE}2. Validation des références entre fichiers{Colors.END}")
    print(f"{'-'*60}")
    
    # Collecter tous les IDs disponibles
    available_ids = set()
    for file_ids in all_ids.values():
        available_ids.update(file_ids)
    
    # Afficher tous les IDs trouvés
    print(f"\n{Colors.YELLOW}IDs définis:{Colors.END}")
    for file_name, ids in sorted(all_ids.items()):
        if ids:
            print(f"  {file_name}:")
            for id_val in sorted(ids):
                print(f"    - {id_val}")
    
    # Vérifier les références
    print(f"\n{Colors.YELLOW}Références (actions, parents, etc.):{Colors.END}")
    missing_refs = set()
    
    for file_name, refs in sorted(all_refs.items()):
        if refs:
            print(f"  {file_name}:")
            for ref_type, ref_id in sorted(refs):
                # Les IDs qualifiés (avec module) ne peuvent pas être vérifiés localement
                if '.' in ref_id:
                    status = f"{Colors.YELLOW}(externe){Colors.END}"
                elif ref_id in available_ids:
                    status = f"{Colors.GREEN}OK{Colors.END}"
                else:
                    status = f"{Colors.RED}MANQUANT{Colors.END}"
                    missing_refs.add((ref_type, ref_id))
                
                print(f"    - {ref_type}: {ref_id} {status}")
    
    if missing_refs:
        print(f"\n{Colors.RED}❌ Références manquantes:{Colors.END}")
        for ref_type, ref_id in sorted(missing_refs):
            print(f"  - {ref_type}: {ref_id}")
        return False
    
    print(f"\n{Colors.GREEN}✓ Toutes les références sont valides{Colors.END}\n")
    
    # Étape 3: Vérifications supplémentaires
    print(f"{Colors.BLUE}3. Vérifications supplémentaires{Colors.END}")
    print(f"{'-'*60}")
    
    # Vérifier que les fichiers requis existent
    required_files = [
        'views/menu_views.xml',
        'views/investisseur_views.xml',
        'wizards/import_excel_wizard_views.xml',
    ]
    
    for req_file in required_files:
        file_path = module_path / req_file
        if file_path.exists():
            print(f"{Colors.GREEN}✓ {req_file}{Colors.END}")
        else:
            print(f"{Colors.RED}✗ {req_file} - MANQUANT{Colors.END}")
            all_valid = False
    
    print()
    
    if all_valid:
        print(f"{Colors.GREEN}{'='*60}")
        print(f"✓ Module prêt pour le build Docker!")
        print(f"{'='*60}{Colors.END}\n")
        return True
    else:
        print(f"{Colors.RED}{'='*60}")
        print(f"❌ Erreurs détectées - Corrigez-les avant le build")
        print(f"{'='*60}{Colors.END}\n")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
