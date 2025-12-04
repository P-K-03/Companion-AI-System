extract_message_features_json = {"communication_style_preferences": "","emotional_state_indicators": "","explicit_facts": "", "implicit_preferences": "",}

extract_message_features_prompt = f"""You will given a list of messages. For each message, extract and identify:
1. Communication Style Preferences: How the user prefers to communicate (formal/informal, concise/detailed, direct/indirect, technical/casual, etc.)
2. Emotional State Indicators: Signs of the user's emotional state (positive, negative, neutral, frustrated, excited, confused, etc.)
3. Explicit Facts: Clear, stated facts about the user (interests, location, occupation, relationships, schedules, etc.)
4. Implicit Preferences: Unstated preferences inferred from context (topics they engage with, communication patterns, values, priorities, etc.)
Follow these Guidelines:
- Be specific and evidence-based in your analysis
- Distinguish clearly between explicit statements and inferences
- Include confidence levels for uncertain interpretations
- Avoid over-interpretation - mark low confidence when uncertain
- Don't infer gender from ambiguous statements and distinguish stated preferences from one-off comments.
- If a category has no relevant information for a message, use an empty array
- Do not explain your output, respond only with the supplied JSON and do not prettify the JSON.
 Only return the output as a JSON of the format- {extract_message_features_json}
 Here is the list of messages- """

extract_aggregate_pattern_prompt = f"""You have extracted information from 30 individual chat messages. Now synthesize these into a cohesive user profile.

Your task:
    1. Identify PATTERNS across multiple messages (e.g., "consistently asks about X topic")
    2. Resolve CONTRADICTIONS (e.g., early messages show preference A, later messages show preference B)
    3. Assess CONFIDENCE (high confidence = mentioned multiple times, low = mentioned once)
    4. Extract TEMPORAL patterns (e.g., "asks about productivity on Mondays", "becomes more casual over time")
    5. Prioritize the most IMPORTANT/ACTIONABLE insights
    Special cases to handle:
    - If a fact is mentioned once, mark confidence as 0.3-0.5
    - If user explicitly corrects themselves, prioritize the correction
    - If user talks about future plans, mark as "aspirational" not current fact
    - If emotional patterns only appear once, don't generalize to a "pattern"
    - Group related facts (e.g., "has cat named Whiskers" + "cat is 3 years old" + "cat is picky eater" should be connected)
    Only return the output as a JSON of the format 
    Here are the insights: {extract}
    """    