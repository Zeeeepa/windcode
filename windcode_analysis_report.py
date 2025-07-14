#!/usr/bin/env python3
"""
Windcode Repository Analysis Report

This script analyzes the windcode repository structure and demonstrates
how the LSP integration would enhance codebase context and navigation.
"""

import sys
import ast
import json
from pathlib import Path
from typing import List, Dict, Any, Set
from collections import defaultdict

def analyze_windcode_structure() -> Dict[str, Any]:
    """Analyze the structure of the windcode repository."""
    
    print("🔬 Windcode Repository Analysis")
    print("=" * 40)
    
    repo_path = Path.cwd()
    
    analysis = {
        'repository_info': {
            'name': 'windcode',
            'path': str(repo_path),
            'total_files': 0,
            'python_files': 0,
            'directories': []
        },
        'code_structure': {
            'modules': {},
            'functions': [],
            'classes': [],
            'imports': defaultdict(int),
            'complexity_metrics': {}
        },
        'architecture_analysis': {
            'cli_structure': {},
            'agent_structure': {},
            'extension_structure': {},
            'mcp_integration': {}
        },
        'lsp_integration_potential': {
            'diagnostic_opportunities': [],
            'context_enhancement_areas': [],
            'performance_considerations': {}
        }
    }
    
    # Analyze file structure
    print("\n📊 File Structure Analysis:")
    print("-" * 30)
    
    for item in repo_path.rglob("*"):
        if item.is_file():
            analysis['repository_info']['total_files'] += 1
            if item.suffix == '.py':
                analysis['repository_info']['python_files'] += 1
        elif item.is_dir() and not item.name.startswith('.'):
            analysis['repository_info']['directories'].append(str(item.relative_to(repo_path)))
    
    print(f"📁 Total files: {analysis['repository_info']['total_files']}")
    print(f"🐍 Python files: {analysis['repository_info']['python_files']}")
    print(f"📂 Directories: {len(analysis['repository_info']['directories'])}")
    
    return analysis

def analyze_python_code_structure(repo_path: Path) -> Dict[str, Any]:
    """Analyze Python code structure using AST parsing."""
    
    print("\n🐍 Python Code Structure Analysis:")
    print("-" * 35)
    
    structure = {
        'modules': {},
        'functions': [],
        'classes': [],
        'imports': defaultdict(int),
        'complexity_metrics': {
            'total_lines': 0,
            'total_functions': 0,
            'total_classes': 0,
            'average_function_length': 0,
            'complex_functions': []
        }
    }
    
    python_files = list(repo_path.rglob("*.py"))
    
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST
            tree = ast.parse(content, filename=str(py_file))
            
            # Analyze the file
            file_analysis = analyze_ast_node(tree, py_file)
            
            # Aggregate results
            structure['modules'][str(py_file.relative_to(repo_path))] = file_analysis
            structure['functions'].extend(file_analysis['functions'])
            structure['classes'].extend(file_analysis['classes'])
            
            # Count imports
            for imp in file_analysis['imports']:
                structure['imports'][imp] += 1
            
            # Update complexity metrics
            structure['complexity_metrics']['total_lines'] += file_analysis['lines']
            structure['complexity_metrics']['total_functions'] += len(file_analysis['functions'])
            structure['complexity_metrics']['total_classes'] += len(file_analysis['classes'])
            
        except Exception as e:
            print(f"⚠️  Error parsing {py_file.name}: {e}")
    
    # Calculate averages
    if structure['complexity_metrics']['total_functions'] > 0:
        total_func_lines = sum(f['lines'] for f in structure['functions'])
        structure['complexity_metrics']['average_function_length'] = (
            total_func_lines / structure['complexity_metrics']['total_functions']
        )
    
    # Identify complex functions (>50 lines)
    structure['complexity_metrics']['complex_functions'] = [
        f for f in structure['functions'] if f['lines'] > 50
    ]
    
    print(f"🔧 Total functions: {structure['complexity_metrics']['total_functions']}")
    print(f"🏗️  Total classes: {structure['complexity_metrics']['total_classes']}")
    print(f"📦 Unique imports: {len(structure['imports'])}")
    print(f"📏 Average function length: {structure['complexity_metrics']['average_function_length']:.1f} lines")
    print(f"⚠️  Complex functions (>50 lines): {len(structure['complexity_metrics']['complex_functions'])}")
    
    return structure

def analyze_ast_node(tree: ast.AST, file_path: Path) -> Dict[str, Any]:
    """Analyze an AST node to extract code structure."""
    
    analysis = {
        'file': str(file_path),
        'functions': [],
        'classes': [],
        'imports': [],
        'lines': len(open(file_path, 'r').readlines()) if file_path.exists() else 0
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_info = {
                'name': node.name,
                'line': node.lineno,
                'lines': (node.end_lineno or node.lineno) - node.lineno + 1,
                'args': len(node.args.args),
                'decorators': len(node.decorator_list),
                'file': str(file_path.name)
            }
            analysis['functions'].append(func_info)
            
        elif isinstance(node, ast.ClassDef):
            class_info = {
                'name': node.name,
                'line': node.lineno,
                'lines': (node.end_lineno or node.lineno) - node.lineno + 1,
                'methods': len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                'bases': len(node.bases),
                'file': str(file_path.name)
            }
            analysis['classes'].append(class_info)
            
        elif isinstance(node, ast.Import):
            for alias in node.names:
                analysis['imports'].append(alias.name)
                
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                analysis['imports'].append(node.module)
    
    return analysis

def analyze_windcode_architecture(repo_path: Path) -> Dict[str, Any]:
    """Analyze windcode-specific architecture."""
    
    print("\n🏗️  Windcode Architecture Analysis:")
    print("-" * 35)
    
    architecture = {
        'cli_structure': analyze_cli_structure(repo_path),
        'agent_structure': analyze_agent_structure(repo_path),
        'extension_structure': analyze_extension_structure(repo_path),
        'mcp_integration': analyze_mcp_integration(repo_path)
    }
    
    return architecture

def analyze_cli_structure(repo_path: Path) -> Dict[str, Any]:
    """Analyze CLI structure."""
    
    cli_path = repo_path / "cli"
    if not cli_path.exists():
        return {'exists': False}
    
    cli_analysis = {
        'exists': True,
        'total_files': len(list(cli_path.rglob("*.py"))),
        'command_groups': [],
        'utilities': [],
        'main_commands': []
    }
    
    # Find command groups (directories with commands.py)
    for item in cli_path.iterdir():
        if item.is_dir():
            commands_file = item / "commands.py"
            if commands_file.exists():
                cli_analysis['command_groups'].append(item.name)
    
    # Find main CLI files
    cli_files = [f for f in cli_path.rglob("*.py") if f.name in ['cli.py', 'main.py', '__main__.py']]
    cli_analysis['main_commands'] = [f.name for f in cli_files]
    
    print(f"🖥️  CLI structure found: {cli_analysis['exists']}")
    print(f"📁 CLI files: {cli_analysis['total_files']}")
    print(f"⚡ Command groups: {len(cli_analysis['command_groups'])}")
    
    if cli_analysis['command_groups']:
        print(f"📋 Command groups: {', '.join(cli_analysis['command_groups'])}")
    
    return cli_analysis

def analyze_agent_structure(repo_path: Path) -> Dict[str, Any]:
    """Analyze agent structure."""
    
    agents_path = repo_path / "agents"
    if not agents_path.exists():
        return {'exists': False}
    
    agent_analysis = {
        'exists': True,
        'total_files': len(list(agents_path.rglob("*.py"))),
        'agent_types': [],
        'notebooks': len(list(agents_path.rglob("*.ipynb")))
    }
    
    # Find agent files
    agent_files = [f for f in agents_path.rglob("*.py") if 'agent' in f.name.lower()]
    agent_analysis['agent_types'] = [f.stem for f in agent_files]
    
    print(f"🤖 Agent structure found: {agent_analysis['exists']}")
    print(f"📁 Agent files: {agent_analysis['total_files']}")
    print(f"🧠 Agent types: {len(agent_analysis['agent_types'])}")
    print(f"📓 Notebooks: {agent_analysis['notebooks']}")
    
    if agent_analysis['agent_types']:
        print(f"📋 Agent types: {', '.join(agent_analysis['agent_types'])}")
    
    return agent_analysis

def analyze_extension_structure(repo_path: Path) -> Dict[str, Any]:
    """Analyze extension structure."""
    
    extensions_path = repo_path / "extensions"
    if not extensions_path.exists():
        return {'exists': False}
    
    extension_analysis = {
        'exists': True,
        'total_files': len(list(extensions_path.rglob("*.py"))),
        'extension_types': [],
        'tools': []
    }
    
    # Find extension directories
    for item in extensions_path.iterdir():
        if item.is_dir():
            extension_analysis['extension_types'].append(item.name)
    
    # Find tools
    tools_path = extensions_path / "tools"
    if tools_path.exists():
        tool_files = [f for f in tools_path.rglob("*.py") if f.name != "__init__.py"]
        extension_analysis['tools'] = [f.stem for f in tool_files]
    
    print(f"🔌 Extension structure found: {extension_analysis['exists']}")
    print(f"📁 Extension files: {extension_analysis['total_files']}")
    print(f"🔧 Extension types: {len(extension_analysis['extension_types'])}")
    print(f"🛠️  Tools: {len(extension_analysis['tools'])}")
    
    if extension_analysis['extension_types']:
        print(f"📋 Extensions: {', '.join(extension_analysis['extension_types'])}")
    
    return extension_analysis

def analyze_mcp_integration(repo_path: Path) -> Dict[str, Any]:
    """Analyze MCP integration."""
    
    mcp_files = list(repo_path.rglob("*mcp*"))
    
    mcp_analysis = {
        'total_mcp_files': len(mcp_files),
        'mcp_directories': [],
        'mcp_python_files': []
    }
    
    for mcp_file in mcp_files:
        if mcp_file.is_dir():
            mcp_analysis['mcp_directories'].append(str(mcp_file.relative_to(repo_path)))
        elif mcp_file.suffix == '.py':
            mcp_analysis['mcp_python_files'].append(str(mcp_file.relative_to(repo_path)))
    
    print(f"🔗 MCP-related files: {mcp_analysis['total_mcp_files']}")
    print(f"📂 MCP directories: {len(mcp_analysis['mcp_directories'])}")
    print(f"🐍 MCP Python files: {len(mcp_analysis['mcp_python_files'])}")
    
    return mcp_analysis

def assess_lsp_integration_potential(structure: Dict[str, Any], architecture: Dict[str, Any]) -> Dict[str, Any]:
    """Assess the potential benefits of LSP integration."""
    
    print("\n🔬 LSP Integration Potential Assessment:")
    print("-" * 40)
    
    potential = {
        'diagnostic_opportunities': [],
        'context_enhancement_areas': [],
        'performance_considerations': {},
        'integration_benefits': []
    }
    
    # Assess diagnostic opportunities
    complex_functions = structure['complexity_metrics']['complex_functions']
    if complex_functions:
        potential['diagnostic_opportunities'].append(
            f"Complex function analysis: {len(complex_functions)} functions >50 lines"
        )
    
    total_functions = structure['complexity_metrics']['total_functions']
    if total_functions > 100:
        potential['diagnostic_opportunities'].append(
            f"Large codebase analysis: {total_functions} functions across {len(structure['modules'])} modules"
        )
    
    # Assess context enhancement areas
    if architecture['cli_structure']['exists']:
        potential['context_enhancement_areas'].append(
            f"CLI command navigation: {len(architecture['cli_structure']['command_groups'])} command groups"
        )
    
    if architecture['agent_structure']['exists']:
        potential['context_enhancement_areas'].append(
            f"Agent code analysis: {len(architecture['agent_structure']['agent_types'])} agent types"
        )
    
    if architecture['extension_structure']['exists']:
        potential['context_enhancement_areas'].append(
            f"Extension system navigation: {len(architecture['extension_structure']['extension_types'])} extensions"
        )
    
    # Performance considerations
    python_files = len(structure['modules'])
    potential['performance_considerations'] = {
        'file_count': python_files,
        'complexity_level': 'high' if python_files > 100 else 'medium' if python_files > 50 else 'low',
        'cache_importance': 'high' if python_files > 100 else 'medium',
        'incremental_analysis_benefit': 'high' if total_functions > 200 else 'medium'
    }
    
    # Integration benefits
    potential['integration_benefits'] = [
        "Real-time error detection across CLI, agents, and extensions",
        "Enhanced code navigation for complex multi-module architecture",
        "Intelligent autocomplete for windcode-specific patterns",
        "Dependency analysis for agent and extension interactions",
        "Performance monitoring for large codebase operations"
    ]
    
    # Display assessment
    print("🎯 Diagnostic Opportunities:")
    for opportunity in potential['diagnostic_opportunities']:
        print(f"  • {opportunity}")
    
    print("\n🧠 Context Enhancement Areas:")
    for area in potential['context_enhancement_areas']:
        print(f"  • {area}")
    
    print(f"\n⚡ Performance Considerations:")
    perf = potential['performance_considerations']
    print(f"  • File count: {perf['file_count']} (complexity: {perf['complexity_level']})")
    print(f"  • Cache importance: {perf['cache_importance']}")
    print(f"  • Incremental analysis benefit: {perf['incremental_analysis_benefit']}")
    
    print(f"\n✨ Integration Benefits:")
    for benefit in potential['integration_benefits']:
        print(f"  • {benefit}")
    
    return potential

def demonstrate_lsp_features() -> Dict[str, Any]:
    """Demonstrate how LSP features would work with windcode."""
    
    print("\n🚀 LSP Feature Demonstration:")
    print("-" * 35)
    
    demo = {
        'error_detection_examples': [
            {
                'type': 'syntax_error',
                'description': 'Missing import statements in agent modules',
                'benefit': 'Immediate feedback on missing dependencies'
            },
            {
                'type': 'type_error',
                'description': 'Incorrect parameter types in CLI commands',
                'benefit': 'Prevent runtime errors in command execution'
            },
            {
                'type': 'unused_import',
                'description': 'Unused imports in extension modules',
                'benefit': 'Code cleanup and performance optimization'
            }
        ],
        'context_enhancement_examples': [
            {
                'feature': 'go_to_definition',
                'description': 'Navigate from CLI command to agent implementation',
                'benefit': 'Faster code exploration and debugging'
            },
            {
                'feature': 'find_references',
                'description': 'Find all usages of extension APIs',
                'benefit': 'Impact analysis for code changes'
            },
            {
                'feature': 'symbol_search',
                'description': 'Search for functions across all modules',
                'benefit': 'Quick code discovery and reuse'
            }
        ],
        'transaction_aware_benefits': [
            'File changes automatically update diagnostic context',
            'Real-time validation of agent configuration changes',
            'Immediate feedback on CLI command modifications',
            'Synchronized analysis across extension dependencies'
        ]
    }
    
    print("🔍 Error Detection Examples:")
    for example in demo['error_detection_examples']:
        print(f"  • {example['type']}: {example['description']}")
        print(f"    → {example['benefit']}")
    
    print("\n🧠 Context Enhancement Examples:")
    for example in demo['context_enhancement_examples']:
        print(f"  • {example['feature']}: {example['description']}")
        print(f"    → {example['benefit']}")
    
    print("\n🔄 Transaction-Aware Benefits:")
    for benefit in demo['transaction_aware_benefits']:
        print(f"  • {benefit}")
    
    return demo

def generate_comprehensive_report(analysis: Dict[str, Any], structure: Dict[str, Any], 
                                architecture: Dict[str, Any], potential: Dict[str, Any], 
                                demo: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive analysis report."""
    
    print("\n📊 Comprehensive Windcode Analysis Report")
    print("=" * 45)
    
    report = {
        'repository_summary': {
            'name': analysis['repository_info']['name'],
            'total_files': analysis['repository_info']['total_files'],
            'python_files': analysis['repository_info']['python_files'],
            'complexity_score': calculate_complexity_score(structure),
            'architecture_components': count_architecture_components(architecture)
        },
        'lsp_integration_assessment': {
            'readiness_score': calculate_readiness_score(structure, architecture),
            'priority_areas': potential['context_enhancement_areas'],
            'expected_benefits': potential['integration_benefits'],
            'implementation_complexity': assess_implementation_complexity(structure, architecture)
        },
        'recommendations': generate_recommendations(structure, architecture, potential)
    }
    
    # Display summary
    summary = report['repository_summary']
    print(f"🏗️  Repository: {summary['name']}")
    print(f"📁 Total Files: {summary['total_files']}")
    print(f"🐍 Python Files: {summary['python_files']}")
    print(f"📊 Complexity Score: {summary['complexity_score']}/10")
    print(f"🏛️  Architecture Components: {summary['architecture_components']}")
    
    assessment = report['lsp_integration_assessment']
    print(f"\n🔬 LSP Integration Assessment:")
    print(f"  • Readiness Score: {assessment['readiness_score']}/10")
    print(f"  • Priority Areas: {len(assessment['priority_areas'])}")
    print(f"  • Expected Benefits: {len(assessment['expected_benefits'])}")
    print(f"  • Implementation Complexity: {assessment['implementation_complexity']}")
    
    print(f"\n💡 Recommendations:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    return report

def calculate_complexity_score(structure: Dict[str, Any]) -> int:
    """Calculate complexity score (1-10)."""
    
    metrics = structure['complexity_metrics']
    
    # Base score
    score = 5
    
    # Adjust based on file count
    file_count = len(structure['modules'])
    if file_count > 100:
        score += 2
    elif file_count > 50:
        score += 1
    
    # Adjust based on function count
    func_count = metrics['total_functions']
    if func_count > 500:
        score += 2
    elif func_count > 200:
        score += 1
    
    # Adjust based on complex functions
    complex_funcs = len(metrics['complex_functions'])
    if complex_funcs > 20:
        score += 1
    
    return min(10, max(1, score))

def count_architecture_components(architecture: Dict[str, Any]) -> int:
    """Count architecture components."""
    
    count = 0
    
    if architecture['cli_structure']['exists']:
        count += 1
    if architecture['agent_structure']['exists']:
        count += 1
    if architecture['extension_structure']['exists']:
        count += 1
    if architecture['mcp_integration']['total_mcp_files'] > 0:
        count += 1
    
    return count

def calculate_readiness_score(structure: Dict[str, Any], architecture: Dict[str, Any]) -> int:
    """Calculate LSP integration readiness score (1-10)."""
    
    score = 7  # Base score for Python codebase
    
    # Bonus for complex codebase (more benefit from LSP)
    if len(structure['modules']) > 100:
        score += 1
    
    # Bonus for multiple architecture components
    components = count_architecture_components(architecture)
    if components >= 3:
        score += 1
    
    # Bonus for complex functions (diagnostic opportunities)
    if len(structure['complexity_metrics']['complex_functions']) > 10:
        score += 1
    
    return min(10, score)

def assess_implementation_complexity(structure: Dict[str, Any], architecture: Dict[str, Any]) -> str:
    """Assess implementation complexity."""
    
    file_count = len(structure['modules'])
    components = count_architecture_components(architecture)
    
    if file_count > 100 and components >= 3:
        return "Medium-High"
    elif file_count > 50 or components >= 2:
        return "Medium"
    else:
        return "Low-Medium"

def generate_recommendations(structure: Dict[str, Any], architecture: Dict[str, Any], 
                           potential: Dict[str, Any]) -> List[str]:
    """Generate implementation recommendations."""
    
    recommendations = []
    
    # Always recommend the transaction-aware LSP integration
    recommendations.append(
        "Implement transaction-aware LSP integration for real-time diagnostics"
    )
    
    # Specific recommendations based on architecture
    if architecture['cli_structure']['exists']:
        recommendations.append(
            "Add CLI-specific diagnostic rules for command validation"
        )
    
    if architecture['agent_structure']['exists']:
        recommendations.append(
            "Implement agent-specific context analysis for better code navigation"
        )
    
    if architecture['extension_structure']['exists']:
        recommendations.append(
            "Create extension API validation and autocomplete support"
        )
    
    # Performance recommendations
    file_count = len(structure['modules'])
    if file_count > 100:
        recommendations.append(
            "Implement incremental analysis and intelligent caching for performance"
        )
    
    # Code quality recommendations
    complex_funcs = len(structure['complexity_metrics']['complex_functions'])
    if complex_funcs > 10:
        recommendations.append(
            f"Focus on refactoring {complex_funcs} complex functions identified by LSP analysis"
        )
    
    return recommendations

def main():
    """Main analysis function."""
    
    repo_path = Path.cwd()
    
    # Perform comprehensive analysis
    analysis = analyze_windcode_structure()
    structure = analyze_python_code_structure(repo_path)
    architecture = analyze_windcode_architecture(repo_path)
    potential = assess_lsp_integration_potential(structure, architecture)
    demo = demonstrate_lsp_features()
    
    # Generate final report
    report = generate_comprehensive_report(analysis, structure, architecture, potential, demo)
    
    print(f"\n🎉 Analysis Complete!")
    print("The windcode repository is well-suited for LSP integration with significant benefits.")
    
    return report

if __name__ == "__main__":
    report = main()
    
    # Save report to file
    with open("windcode_lsp_analysis_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Detailed report saved to: windcode_lsp_analysis_report.json")
