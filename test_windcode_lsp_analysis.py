#!/usr/bin/env python3
"""
Windcode Repository LSP Analysis Test

This script tests the transaction-aware LSP integration with the windcode repository,
validates Serena integration, and demonstrates enhanced codebase context capabilities.
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# Add the graph-sitter src directory to the path
graph_sitter_path = Path(__file__).parent.parent / "graph-sitter" / "src"
if graph_sitter_path.exists():
    sys.path.insert(0, str(graph_sitter_path))

def clone_windcode_repo():
    """Clone the windcode repository for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    repo_url = "https://github.com/Zeeeepa/windcode.git"
    
    print(f"🔄 Cloning {repo_url}...")
    try:
        subprocess.run([
            "git", "clone", repo_url, str(temp_dir / "windcode")
        ], check=True, capture_output=True)
        
        repo_path = temp_dir / "windcode"
        print(f"✅ Repository cloned to: {repo_path}")
        return repo_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone repository: {e}")
        return None

def analyze_repository_structure(repo_path: Path) -> Dict[str, Any]:
    """Analyze the structure of the windcode repository."""
    
    print(f"\n📊 Repository Structure Analysis:")
    print("=" * 40)
    
    structure = {
        'total_files': 0,
        'python_files': [],
        'config_files': [],
        'documentation': [],
        'directories': [],
        'file_types': {}
    }
    
    for item in repo_path.rglob("*"):
        if item.is_file():
            structure['total_files'] += 1
            suffix = item.suffix.lower()
            
            # Count file types
            structure['file_types'][suffix] = structure['file_types'].get(suffix, 0) + 1
            
            # Categorize files
            if suffix == '.py':
                structure['python_files'].append(str(item.relative_to(repo_path)))
            elif suffix in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
                structure['config_files'].append(str(item.relative_to(repo_path)))
            elif suffix in ['.md', '.rst', '.txt'] or item.name.upper() in ['README', 'LICENSE']:
                structure['documentation'].append(str(item.relative_to(repo_path)))
        elif item.is_dir() and not item.name.startswith('.'):
            structure['directories'].append(str(item.relative_to(repo_path)))
    
    # Display structure
    print(f"📁 Total files: {structure['total_files']}")
    print(f"🐍 Python files: {len(structure['python_files'])}")
    print(f"⚙️  Config files: {len(structure['config_files'])}")
    print(f"📚 Documentation: {len(structure['documentation'])}")
    print(f"📂 Directories: {len(structure['directories'])}")
    
    print(f"\n📋 File Type Distribution:")
    for ext, count in sorted(structure['file_types'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {ext or '(no ext)'}: {count}")
    
    print(f"\n📂 Main Directories:")
    for directory in sorted(structure['directories'])[:10]:
        print(f"  📁 {directory}")
    
    return structure

def test_lsp_integration_with_windcode(repo_path: Path):
    """Test LSP integration with the windcode repository."""
    
    print(f"\n🔬 Testing LSP Integration with Windcode")
    print("=" * 50)
    
    try:
        # Import Graph-Sitter components
        from graph_sitter import Codebase
        from graph_sitter.core.diagnostics import add_diagnostic_capabilities
        
        # Initialize codebase with LSP integration
        print(f"📁 Initializing codebase: {repo_path}")
        codebase = Codebase(str(repo_path), enable_lsp=True)
        
        print(f"✅ Codebase initialized successfully")
        print(f"   Name: {codebase.name}")
        print(f"   Language: {codebase.language}")
        print(f"   Files: {len(codebase.files)}")
        
        # Test LSP status and capabilities
        print(f"\n🔍 LSP Integration Status:")
        print("-" * 30)
        
        lsp_status = test_lsp_status(codebase)
        
        # Analyze codebase structure with Graph-Sitter
        print(f"\n📊 Graph-Sitter Analysis:")
        print("-" * 30)
        
        structure_analysis = analyze_codebase_with_graph_sitter(codebase)
        
        # Test diagnostic capabilities
        print(f"\n🩺 Diagnostic Analysis:")
        print("-" * 25)
        
        diagnostic_results = test_diagnostic_capabilities(codebase)
        
        # Test enhanced context capabilities
        print(f"\n🧠 Enhanced Context Analysis:")
        print("-" * 35)
        
        context_analysis = test_enhanced_context(codebase)
        
        # Performance analysis
        print(f"\n⚡ Performance Analysis:")
        print("-" * 25)
        
        performance_results = test_performance_metrics(codebase)
        
        # Generate comprehensive report
        return generate_analysis_report(
            codebase, lsp_status, structure_analysis, 
            diagnostic_results, context_analysis, performance_results
        )
        
    except Exception as e:
        print(f"❌ Error during LSP integration test: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_lsp_status(codebase) -> Dict[str, Any]:
    """Test LSP status and capabilities."""
    
    status = {
        'lsp_available': False,
        'serena_available': False,
        'bridge_initialized': False,
        'features_available': []
    }
    
    if hasattr(codebase, 'is_lsp_enabled'):
        status['lsp_available'] = codebase.is_lsp_enabled()
        print(f"LSP Enabled: {'✅ Yes' if status['lsp_available'] else '❌ No'}")
        
        if status['lsp_available']:
            lsp_status = codebase.get_lsp_status()
            status['serena_available'] = lsp_status.get('serena_available', False)
            status['bridge_initialized'] = lsp_status.get('bridge_initialized', False)
            
            print(f"Serena Available: {'✅ Yes' if status['serena_available'] else '❌ No'}")
            print(f"Bridge Initialized: {'✅ Yes' if status['bridge_initialized'] else '❌ No'}")
            print(f"Active Transactions: {lsp_status.get('active_transactions', 0)}")
            print(f"Change Listeners: {lsp_status.get('change_listeners', 0)}")
            print(f"Cached Files: {lsp_status.get('cached_files', 0)}")
            
            # Test available features
            features = []
            if hasattr(codebase, 'errors'):
                features.append('error_detection')
            if hasattr(codebase, 'warnings'):
                features.append('warning_detection')
            if hasattr(codebase, 'hints'):
                features.append('hint_detection')
            if hasattr(codebase, 'get_file_diagnostics'):
                features.append('file_specific_diagnostics')
            if hasattr(codebase, 'refresh_diagnostics'):
                features.append('diagnostic_refresh')
            
            status['features_available'] = features
            print(f"Available Features: {', '.join(features)}")
        else:
            print("💡 LSP integration disabled - Serena dependencies not available")
    else:
        print("❌ LSP integration not available")
    
    return status

def analyze_codebase_with_graph_sitter(codebase) -> Dict[str, Any]:
    """Analyze codebase structure using Graph-Sitter."""
    
    analysis = {
        'total_files': len(codebase.files),
        'python_files': [],
        'functions': [],
        'classes': [],
        'imports': [],
        'complexity_metrics': {}
    }
    
    # Analyze Python files
    python_files = [f for f in codebase.files if f.path.suffix == '.py']
    analysis['python_files'] = [str(f.path) for f in python_files]
    
    print(f"🐍 Python files found: {len(python_files)}")
    
    # Analyze functions and classes
    try:
        functions = codebase.functions
        classes = codebase.classes
        
        analysis['functions'] = [f.name for f in functions[:20]]  # First 20
        analysis['classes'] = [c.name for c in classes[:20]]  # First 20
        
        print(f"🔧 Functions found: {len(functions)}")
        print(f"🏗️  Classes found: {len(classes)}")
        
        # Show some examples
        if functions:
            print(f"📋 Sample functions:")
            for i, func in enumerate(functions[:5], 1):
                print(f"  {i}. {func.name} (in {func.file.path.name})")
        
        if classes:
            print(f"📋 Sample classes:")
            for i, cls in enumerate(classes[:5], 1):
                print(f"  {i}. {cls.name} (in {cls.file.path.name})")
        
    except Exception as e:
        print(f"⚠️  Error analyzing functions/classes: {e}")
    
    # Analyze imports
    try:
        imports = codebase.imports
        analysis['imports'] = [str(imp) for imp in imports[:20]]  # First 20
        
        print(f"📦 Imports found: {len(imports)}")
        
        # Show import patterns
        import_modules = {}
        for imp in imports:
            module = str(imp).split('.')[0] if '.' in str(imp) else str(imp)
            import_modules[module] = import_modules.get(module, 0) + 1
        
        print(f"📋 Top imported modules:")
        for module, count in sorted(import_modules.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {module}: {count} times")
            
    except Exception as e:
        print(f"⚠️  Error analyzing imports: {e}")
    
    return analysis

def test_diagnostic_capabilities(codebase) -> Dict[str, Any]:
    """Test diagnostic capabilities."""
    
    results = {
        'errors': [],
        'warnings': [],
        'hints': [],
        'file_diagnostics': {},
        'total_diagnostics': 0
    }
    
    if hasattr(codebase, 'errors'):
        errors = codebase.errors
        results['errors'] = [
            {
                'file': error.file_path,
                'line': error.line,
                'message': error.message,
                'severity': error.severity
            } for error in errors[:10]  # First 10 errors
        ]
        print(f"🔴 Errors found: {len(errors)}")
        
        if errors:
            print(f"📋 Sample errors:")
            for i, error in enumerate(errors[:3], 1):
                file_name = Path(error.file_path).name
                print(f"  {i}. {file_name}:{error.line} - {error.message[:60]}{'...' if len(error.message) > 60 else ''}")
    else:
        print("❌ Error detection not available")
    
    if hasattr(codebase, 'warnings'):
        warnings = codebase.warnings
        results['warnings'] = [
            {
                'file': warning.file_path,
                'line': warning.line,
                'message': warning.message,
                'severity': warning.severity
            } for warning in warnings[:10]  # First 10 warnings
        ]
        print(f"🟡 Warnings found: {len(warnings)}")
        
        if warnings:
            print(f"📋 Sample warnings:")
            for i, warning in enumerate(warnings[:3], 1):
                file_name = Path(warning.file_path).name
                print(f"  {i}. {file_name}:{warning.line} - {warning.message[:60]}{'...' if len(warning.message) > 60 else ''}")
    else:
        print("❌ Warning detection not available")
    
    if hasattr(codebase, 'hints'):
        hints = codebase.hints
        results['hints'] = [
            {
                'file': hint.file_path,
                'line': hint.line,
                'message': hint.message,
                'severity': hint.severity
            } for hint in hints[:10]  # First 10 hints
        ]
        print(f"🔵 Hints found: {len(hints)}")
    else:
        print("❌ Hint detection not available")
    
    # Test file-specific diagnostics
    if hasattr(codebase, 'get_file_diagnostics'):
        python_files = [f for f in codebase.files if f.path.suffix == '.py']
        if python_files:
            sample_file = python_files[0]
            file_diagnostics = codebase.get_file_diagnostics(str(sample_file.path))
            results['file_diagnostics'][str(sample_file.path)] = len(file_diagnostics)
            
            print(f"📄 File-specific diagnostics for {sample_file.path.name}: {len(file_diagnostics)}")
    
    # Calculate total diagnostics
    if hasattr(codebase, 'diagnostics'):
        all_diagnostics = codebase.diagnostics
        results['total_diagnostics'] = len(all_diagnostics)
        print(f"📊 Total diagnostics: {len(all_diagnostics)}")
    
    return results

def test_enhanced_context(codebase) -> Dict[str, Any]:
    """Test enhanced context capabilities."""
    
    context = {
        'semantic_analysis': {},
        'code_relationships': {},
        'dependency_graph': {},
        'context_extraction': {}
    }
    
    print("🧠 Testing enhanced context capabilities...")
    
    # Test semantic understanding
    try:
        # Analyze code relationships
        python_files = [f for f in codebase.files if f.path.suffix == '.py']
        if python_files:
            sample_file = python_files[0]
            
            # Get functions in the file
            file_functions = [f for f in codebase.functions if f.file == sample_file]
            context['semantic_analysis']['functions_in_file'] = len(file_functions)
            
            print(f"🔧 Functions in {sample_file.path.name}: {len(file_functions)}")
            
            # Analyze imports for the file
            file_imports = [imp for imp in codebase.imports if imp.file == sample_file]
            context['semantic_analysis']['imports_in_file'] = len(file_imports)
            
            print(f"📦 Imports in {sample_file.path.name}: {len(file_imports)}")
            
    except Exception as e:
        print(f"⚠️  Error in semantic analysis: {e}")
    
    # Test dependency relationships
    try:
        # Analyze class inheritance
        classes_with_inheritance = [c for c in codebase.classes if hasattr(c, 'superclasses') and c.superclasses]
        context['code_relationships']['inheritance_count'] = len(classes_with_inheritance)
        
        print(f"🏗️  Classes with inheritance: {len(classes_with_inheritance)}")
        
    except Exception as e:
        print(f"⚠️  Error in relationship analysis: {e}")
    
    # Test context extraction capabilities
    try:
        # Get symbols and their contexts
        symbols = codebase.symbols
        context['context_extraction']['total_symbols'] = len(symbols)
        
        print(f"🔤 Total symbols: {len(symbols)}")
        
        # Analyze symbol types
        symbol_types = {}
        for symbol in symbols[:100]:  # Sample first 100
            symbol_type = type(symbol).__name__
            symbol_types[symbol_type] = symbol_types.get(symbol_type, 0) + 1
        
        context['context_extraction']['symbol_types'] = symbol_types
        
        print(f"📋 Symbol types:")
        for sym_type, count in sorted(symbol_types.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {sym_type}: {count}")
            
    except Exception as e:
        print(f"⚠️  Error in context extraction: {e}")
    
    return context

def test_performance_metrics(codebase) -> Dict[str, Any]:
    """Test performance metrics."""
    
    metrics = {
        'file_count': len(codebase.files),
        'memory_usage': {},
        'processing_time': {},
        'cache_efficiency': {}
    }
    
    print("⚡ Testing performance metrics...")
    
    # Test processing time for different operations
    import time
    
    # Time file access
    start_time = time.time()
    files = list(codebase.files)
    metrics['processing_time']['file_access'] = time.time() - start_time
    print(f"📁 File access time: {metrics['processing_time']['file_access']:.3f}s")
    
    # Time function analysis
    start_time = time.time()
    functions = list(codebase.functions)
    metrics['processing_time']['function_analysis'] = time.time() - start_time
    print(f"🔧 Function analysis time: {metrics['processing_time']['function_analysis']:.3f}s")
    
    # Test cache efficiency if LSP is available
    if hasattr(codebase, 'get_lsp_status'):
        status = codebase.get_lsp_status()
        metrics['cache_efficiency']['cached_files'] = status.get('cached_files', 0)
        print(f"💾 Cached files: {metrics['cache_efficiency']['cached_files']}")
    
    return metrics

def generate_analysis_report(codebase, lsp_status, structure_analysis, 
                           diagnostic_results, context_analysis, performance_results) -> Dict[str, Any]:
    """Generate comprehensive analysis report."""
    
    print(f"\n📊 Comprehensive Analysis Report")
    print("=" * 40)
    
    report = {
        'repository': {
            'name': codebase.name,
            'language': str(codebase.language),
            'total_files': len(codebase.files),
            'python_files': len([f for f in codebase.files if f.path.suffix == '.py'])
        },
        'lsp_integration': lsp_status,
        'structure_analysis': structure_analysis,
        'diagnostic_results': diagnostic_results,
        'context_analysis': context_analysis,
        'performance_results': performance_results,
        'recommendations': []
    }
    
    # Generate recommendations
    recommendations = []
    
    if not lsp_status['serena_available']:
        recommendations.append("Install Serena dependencies for enhanced LSP capabilities")
    
    if diagnostic_results['total_diagnostics'] > 0:
        recommendations.append(f"Address {diagnostic_results['total_diagnostics']} diagnostic issues")
    
    if performance_results['processing_time'].get('function_analysis', 0) > 1.0:
        recommendations.append("Consider optimizing function analysis performance")
    
    report['recommendations'] = recommendations
    
    # Display summary
    print(f"🏗️  Repository: {report['repository']['name']}")
    print(f"📊 Language: {report['repository']['language']}")
    print(f"📁 Total Files: {report['repository']['total_files']}")
    print(f"🐍 Python Files: {report['repository']['python_files']}")
    print(f"🔧 Functions: {len(structure_analysis.get('functions', []))}")
    print(f"🏗️  Classes: {len(structure_analysis.get('classes', []))}")
    print(f"📦 Imports: {len(structure_analysis.get('imports', []))}")
    
    print(f"\n🩺 Diagnostics Summary:")
    print(f"  🔴 Errors: {len(diagnostic_results['errors'])}")
    print(f"  🟡 Warnings: {len(diagnostic_results['warnings'])}")
    print(f"  🔵 Hints: {len(diagnostic_results['hints'])}")
    print(f"  📊 Total: {diagnostic_results['total_diagnostics']}")
    
    print(f"\n⚡ Performance Summary:")
    for metric, value in performance_results['processing_time'].items():
        print(f"  {metric}: {value:.3f}s")
    
    if recommendations:
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    return report

def main():
    """Main analysis function."""
    
    print("🔬 Windcode Repository LSP Analysis")
    print("Testing transaction-aware LSP integration with enhanced context")
    print("=" * 60)
    
    # Use current directory (windcode repo is already cloned)
    repo_path = Path.cwd()
    
    if not repo_path.exists():
        print("❌ Repository not found. Exiting.")
        return False
    
    try:
        # Analyze repository structure
        structure = analyze_repository_structure(repo_path)
        
        # Test LSP integration
        analysis_report = test_lsp_integration_with_windcode(repo_path)
        
        if analysis_report:
            print(f"\n🎉 SUCCESS: Windcode LSP analysis completed successfully!")
            print("The transaction-aware LSP integration provides enhanced codebase context.")
            
            # Test specific windcode features
            print(f"\n🎯 Windcode-Specific Analysis:")
            print("-" * 35)
            
            test_windcode_specific_features(repo_path, analysis_report)
            
            return True
        else:
            print(f"\n⚠️  PARTIAL SUCCESS: Some features may not be available.")
            print("This could be due to missing Serena dependencies.")
            return False
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_windcode_specific_features(repo_path: Path, analysis_report: Dict[str, Any]):
    """Test windcode-specific features and capabilities."""
    
    print("🎯 Testing windcode-specific features...")
    
    # Analyze CLI structure
    cli_path = repo_path / "cli"
    if cli_path.exists():
        cli_files = list(cli_path.rglob("*.py"))
        print(f"🖥️  CLI Python files: {len(cli_files)}")
        
        # Look for command patterns
        command_files = [f for f in cli_files if 'command' in f.name.lower()]
        print(f"⚡ Command files: {len(command_files)}")
    
    # Analyze agents structure
    agents_path = repo_path / "agents"
    if agents_path.exists():
        agent_files = list(agents_path.rglob("*.py"))
        print(f"🤖 Agent Python files: {len(agent_files)}")
        
        # Look for specific agent types
        for agent_file in agent_files:
            if 'agent' in agent_file.name:
                print(f"  📋 Found agent: {agent_file.name}")
    
    # Analyze extensions structure
    extensions_path = repo_path / "extensions"
    if extensions_path.exists():
        extension_dirs = [d for d in extensions_path.iterdir() if d.is_dir()]
        print(f"🔌 Extension directories: {len(extension_dirs)}")
        
        for ext_dir in extension_dirs:
            print(f"  🔧 Extension: {ext_dir.name}")
    
    # Analyze MCP integration
    mcp_files = list(repo_path.rglob("*mcp*"))
    print(f"🔗 MCP-related files: {len(mcp_files)}")
    
    # Performance assessment
    total_python_files = analysis_report['repository']['python_files']
    if total_python_files > 50:
        print(f"📊 Large codebase detected ({total_python_files} Python files)")
        print("💡 LSP integration will provide significant value for navigation and analysis")
    
    print(f"\n✅ Windcode analysis complete!")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
