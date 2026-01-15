import asyncio
import os
import json
from typing import Any, Dict

class BamlObjectEncoder(json.JSONEncoder):
    """Custom JSON encoder for BAML objects."""
    def default(self, obj):
        # Convert BAML objects to dictionaries
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        # Handle other special types if needed
        elif hasattr(obj, "model_dump"):
            # Support for Pydantic models
            return obj.model_dump()
        # Let the base encoder handle standard types
        return super().default(obj)

def serialize_results(result_obj):
    """Convert potentially complex objects to JSON-serializable format."""
    if hasattr(result_obj, "__dict__"):
        return {k: serialize_results(v) for k, v in result_obj.__dict__.items() if not k.startswith("_")}
    elif isinstance(result_obj, dict):
        return {k: serialize_results(v) for k, v in result_obj.items()}
    elif isinstance(result_obj, list):
        return [serialize_results(item) for item in result_obj]
    elif hasattr(result_obj, "model_dump"):
        return serialize_results(result_obj.model_dump())
    else:
        return result_obj

if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is not set.")
    print("Please set it with: export OPENAI_API_KEY='your-api-key'")
    print("This key is required for the BAML workflow to make API calls to OpenAI.")
    exit(1)

try:
    from baml_client import b
except ImportError:
    print("Warning: baml_client not found. Please run 'baml-cli generate' in the project root after baml_src is populated.")
    b = None

results_store: Dict[str, Any] = {}

async def run_datacollection(initial_input: Any) -> Any:
    print(f"Executing: datacollection...")
    if not b:
        print(f"Skipping Process_datacollection as baml_client is not available.")
        return None
    try:
        result = await b.Process_datacollection(input_payload=initial_input)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"datacollection Result: {result}")
        results_store["datacollection"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_datacollection: {e}")
        results_store["datacollection"] = f"Error: {e}"
        return None

async def run_identifymissingdata(datacollection_output: Any) -> Any:
    print(f"Executing: identifymissingdata...")
    if not b:
        print(f"Skipping Process_identifymissingdata as baml_client is not available.")
        return None
    try:
        result = await b.Process_identifymissingdata(datacollection_output=datacollection_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"identifymissingdata Result: {result}")
        results_store["identifymissingdata"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_identifymissingdata: {e}")
        results_store["identifymissingdata"] = f"Error: {e}"
        return None

async def run_initialdatacleaning(datacollection_output: Any) -> Any:
    print(f"Executing: initialdatacleaning...")
    if not b:
        print(f"Skipping Process_initialdatacleaning as baml_client is not available.")
        return None
    try:
        result = await b.Process_initialdatacleaning(datacollection_output=datacollection_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"initialdatacleaning Result: {result}")
        results_store["initialdatacleaning"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_initialdatacleaning: {e}")
        results_store["initialdatacleaning"] = f"Error: {e}"
        return None

async def run_analyzedataforindustry(initialdatacleaning_output: Any) -> Any:
    print(f"Executing: analyzedataforindustry...")
    if not b:
        print(f"Skipping Process_analyzedataforindustry as baml_client is not available.")
        return None
    try:
        result = await b.Process_analyzedataforindustry(initialdatacleaning_output=initialdatacleaning_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"analyzedataforindustry Result: {result}")
        results_store["analyzedataforindustry"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_analyzedataforindustry: {e}")
        results_store["analyzedataforindustry"] = f"Error: {e}"
        return None

async def run_industryclassification(initialdatacleaning_output: Any) -> Any:
    print(f"Executing: industryclassification...")
    if not b:
        print(f"Skipping Process_industryclassification as baml_client is not available.")
        return None
    try:
        result = await b.Process_industryclassification(initialdatacleaning_output=initialdatacleaning_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"industryclassification Result: {result}")
        results_store["industryclassification"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_industryclassification: {e}")
        results_store["industryclassification"] = f"Error: {e}"
        return None

async def run_generatereport(analyzedataforindustry_output: Any, industryclassification_output: Any) -> Any:
    print(f"Executing: generatereport...")
    if not b:
        print(f"Skipping Process_generatereport as baml_client is not available.")
        return None
    try:
        result = await b.Process_generatereport(analyzedataforindustry_output=analyzedataforindustry_output, industryclassification_output=industryclassification_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"generatereport Result: {result}")
        results_store["generatereport"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_generatereport: {e}")
        results_store["generatereport"] = f"Error: {e}"
        return None

async def main(initial_workflow_input: Any):
    print("Starting BAML DAG workflow...")
    # --- Level 0 ---
    level_0_tasks = []
    level_0_tasks.append(run_datacollection(initial_workflow_input))
    await asyncio.gather(*level_0_tasks)
    # --- Level 1 ---
    level_1_tasks = []
    level_1_tasks.append(run_identifymissingdata(results_store['datacollection']))
    level_1_tasks.append(run_initialdatacleaning(results_store['datacollection']))
    await asyncio.gather(*level_1_tasks)
    # --- Level 2 ---
    level_2_tasks = []
    level_2_tasks.append(run_analyzedataforindustry(results_store['initialdatacleaning']))
    level_2_tasks.append(run_industryclassification(results_store['initialdatacleaning']))
    await asyncio.gather(*level_2_tasks)
    # --- Level 3 ---
    level_3_tasks = []
    level_3_tasks.append(run_generatereport(results_store['analyzedataforindustry'], results_store['industryclassification']))
    await asyncio.gather(*level_3_tasks)

    print("\nWorkflow execution finished.")
    print("Final results_store:")
    # Use the custom JSON encoder to safely serialize BAML objects
    try:
        print(json.dumps(results_store, indent=2, cls=BamlObjectEncoder))
    except TypeError as e:
        print(f"Error serializing results: {e}")
        print("Simplified results:")
        for k, v in results_store.items():
            print(f"  {k}: {type(v).__name__}")
    return results_store

if __name__ == "__main__":
    print("Enter initial input for the workflow (JSON string or plain text):")
    cli_input_str = input()
    try:
        initial_input_data = json.loads(cli_input_str)
    except json.JSONDecodeError:
        initial_input_data = cli_input_str
    asyncio.run(main(initial_input_data))