#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation Python pour le module gaoh_conseil
Vérifie la syntaxe Python et les imports.
"""

import os
import sys
import ast
import py_compile
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def validate_python_syntax(file_path):
    """Valide la syntaxe Python d'un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"Ligne {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def check_imports(file_path):
    """Extrait les imports d'un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(('import', alias.name))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(('from', module, alias.name))
        
        return imports
    except:
        return []

def main():
    module_path = Path(__file__).parent
    py_files = list(module_path.glob('models/*.py')) + \
               list(module_path.glob('wizards/*.py')) + \
               [module_path / '__init__.py', module_path / '__manifest__.py']
    
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"Validation Python du module gaoh_conseil")
    print(f"{'='*60}{Colors.END}\n")
    
    # Étape 1: Validation syntaxe Python
    print(f"{Colors.BLUE}1. Validation de la syntaxe Python{Colors.END}")
    print(f"{'-'*60}")
    
    all_valid = True
    all_imports = {}
    
    for py_file in sorted(py_files):
        if not py_file.exists():
            continue
        
        is_valid, error = validate_python_syntax(py_file)
        file_name = py_file.relative_to(module_path)
        
        if is_valid:
            print(f"{Colors.GREEN}✓ {file_name}{Colors.END}")
            imports = check_imports(py_file)
            if imports:
                all_imports[str(file_name)] = imports
        else:
            print(f"{Colors.RED}✗ {file_name}{Colors.END}")
            print(f"  Erreur: {error}")
            all_valid = False
    
    if not all_valid:
        print(f"\n{Colors.RED}❌ Erreurs Python détectées!{Colors.END}\n")
        return False
    
    print(f"\n{Colors.GREEN}✓ Tous les fichiers Python sont valides{Colors.END}\n")
    
    # Étape 2: Afficher les imports
    print(f"{Colors.BLUE}2. Imports détectés{Colors.END}")
    print(f"{'-'*60}")
    
    for file_name, imports in sorted(all_imports.items()):
        print(f"\n{Colors.YELLOW}{file_name}:{Colors.END}")
        for imp in sorted(set(imports)):
            if imp[0] == 'import':
                print(f"  import {imp[1]}")
            else:
                print(f"  from {imp[1]} import {imp[2]}")
    
    # Étape 3: Vérifier le manifest
    print(f"\n{Colors.BLUE}3. Vérification du __manifest__.py{Colors.END}")
    print(f"{'-'*60}")
    
    manifest_path = module_path / '__manifest__.py'
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_code = f.read()
            
            # Évaluer le dictionnaire du manifest
            manifest_dict = eval(manifest_code)
            
            required_keys = ['name', 'version', 'category', 'author', 'depends', 'data', 'installable', 'license']
            
            for key in required_keys:
                if key in manifest_dict:
                    if key == 'data' and isinstance(manifest_dict[key], list):
                        print(f"{Colors.GREEN}✓ {key}: {len(manifest_dict[key])} fichier(s){Colors.END}")
                        for data_file in manifest_dict[key]:
                            file_path = module_path / data_file
                            if file_path.exists():
                                print(f"    {Colors.GREEN}✓{Colors.END} {data_file}")
                            else:
                                print(f"    {Colors.RED}✗{Colors.END} {data_file} - MANQUANT")
                                all_valid = False
                    else:
                        print(f"{Colors.GREEN}✓ {key}: {manifest_dict[key]}{Colors.END}")
                else:
                    print(f"{Colors.RED}✗ {key}: MANQUANT{Colors.END}")
                    all_valid = False
        except Exception as e:
            print(f"{Colors.RED}✗ Erreur en lisant le manifest: {e}{Colors.END}")
            all_valid = False
    else:
        print(f"{Colors.RED}✗ __manifest__.py non trouvé{Colors.END}")
        all_valid = False
    
    print()
    
    if all_valid:
        print(f"{Colors.GREEN}{'='*60}")
        print(f"✓ Module Python valide!")
        print(f"{'='*60}{Colors.END}\n")
        return True
    else:
        print(f"{Colors.RED}{'='*60}")
        print(f"❌ Erreurs détectées")
        print(f"{'='*60}{Colors.END}\n")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
