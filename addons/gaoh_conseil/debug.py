#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de débogage complet pour le module gaoh_conseil
Lance toutes les validations avant le build Docker.
"""

import os
import sys
import subprocess
from pathlib import Path

# Couleurs
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def run_script(script_path, description):
    """Exécute un script de validation"""
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"{Colors.BOLD}{description}{Colors.END}")
    print(f"{'='*70}{Colors.END}\n")
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=False, 
                              timeout=30)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}Timeout - Le script a dépassé le temps limite{Colors.END}")
        return False
    except Exception as e:
        print(f"{Colors.RED}Erreur: {e}{Colors.END}")
        return False

def main():
    module_path = Path(__file__).parent
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "🔍 DÉBOGAGE MODULE GAOH CONSEIL" + " "*21 + "║")
    print("╚" + "═"*68 + "╝")
    print(f"{Colors.END}\n")
    
    results = {}
    
    # Valider XML
    xml_script = module_path / 'validate_xml.py'
    if xml_script.exists():
        results['XML'] = run_script(xml_script, "📋 Validation XML")
    
    # Valider Python
    python_script = module_path / 'validate_python.py'
    if python_script.exists():
        results['Python'] = run_script(python_script, "🐍 Validation Python")
    
    # Valider Odoo 18
    odoo18_script = module_path / 'debug_odoo18.py'
    if odoo18_script.exists():
        results['Odoo 18'] = run_script(odoo18_script, "🚀 Débogage Odoo 18")
    
    # Résumé
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"{Colors.BOLD}📊 RÉSUMÉ DES VALIDATIONS{Colors.END}")
    print(f"{'='*70}{Colors.END}\n")
    
    all_passed = True
    for check_name, passed in results.items():
        status = f"{Colors.GREEN}✓ RÉUSSI{Colors.END}" if passed else f"{Colors.RED}✗ ÉCHOUÉ{Colors.END}"
        print(f"  {check_name:20} {status}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("╔" + "═"*68 + "╗")
        print("║" + " "*20 + "✓ PRÊT POUR LE BUILD DOCKER" + " "*19 + "║")
        print("╚" + "═"*68 + "╝")
        print(f"{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}")
        print("╔" + "═"*68 + "╗")
        print("║" + " "*15 + "❌ ERREURS DÉTECTÉES - CORRIGEZ-LES D'ABORD" + " "*10 + "║")
        print("╚" + "═"*68 + "╝")
        print(f"{Colors.END}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
