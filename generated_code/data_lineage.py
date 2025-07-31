from typing import Dict, List

class DataTransformation:
    """Represents a data transformation step."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.input_data: List[Dict] = []
        self.output_data: List[Dict] = []

    def execute(self, input_data: List[Dict]) -> List[Dict]:
        """Executes the data transformation."""
        # Implement transformation logic here
        # Example: filtering, mapping, aggregation, etc.
        self.input_data = input_data
        self.output_data = transformed_data
        return self.output_data

# Example usage
transformation1 = DataTransformation("filter_data", "Filters data based on a condition")
transformation2 = DataTransformation("aggregate_data", "Aggregates data by a specific field")

# Maintain a lineage record for each data transformation
lineage_record = []

# Append transformations to lineage record
lineage_record.append(transformation1)
lineage_record.append(transformation2)

# Use lineage_record to track data flow and identify bottlenecks