from integrations.plugins.research_export import ResearchExportPlugin
from integrations.plugins.dashboard_plugin import DashboardPlugin

# Dictionary of available plugins
plugins = {
    "research": ResearchExportPlugin(),
    # future plugins can be added here
    # "ml_pipeline": MLPipelinePlugin(),
    "dashboard": DashboardPlugin(),
}

def get_plugin(name):
    """
    Return plugin instance by name.
    """
    return plugins.get(name)