function Process_analyzedataforindustry(initialdatacleaning_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Identify meaningful patterns and trends in the data.

    Input:
    {{ initialdatacleaning_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_datacollection(input_payload: string) -> string {
  client DefaultOpenAI
  prompt #"
    Collect and preprocess the data for analysis.

    Input:
    {{ input_payload }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_generatereport(industryclassification_output: string, analyzedataforindustry_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Compose a comprehensive and clear report for stakeholders.

    Input:
    {{ industryclassification_output }}
    {{ analyzedataforindustry_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_identifymissingdata(datacollection_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Determine the necessary actions to rectify data inconsistencies.

    Input:
    {{ datacollection_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_industryclassification(initialdatacleaning_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Categorize the companies by industry for comparative analysis.

    Input:
    {{ initialdatacleaning_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_initialdatacleaning(datacollection_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Clean and process the raw data for analysis.

    Input:
    {{ datacollection_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}
