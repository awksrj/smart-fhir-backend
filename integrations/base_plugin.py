class BasePlugin:
    def execute(self, data, config):
        """
        Executes plugin-specific logic on FHIR data.

        Args:
            data (list): List of normalized FHIR resources (dicts).
            config (dict): Optional configuration data (e.g., patient map).

        Returns:
            dict: Plugin-specific output
        """
        raise NotImplementedError("This method should be implemented by the plugin.")