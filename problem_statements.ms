AGENTIC AI HACKATHON
Tech Zephyr 4.0 

Round 1: PROBLEM STATEMENTS
IIT Bhubaneswar
Agentic principle: A strong Agentic AI problem must provide more than generating a good response. The submitted system should autonomously pursue a goal by interacting with multiple tools or a simulated environment, making decisions from intermediate results, taking actions, maintaining task state, adapting to changing conditions, and verifying outcomes.
Common Agentic Requirements
Goal-driven execution rather than one-shot answer generation.
Meaningful tool/environment interaction through APIs, databases, simulators, retrieval systems, calculators, or other provided capabilities.
Persistent task state sufficient to reason over intermediate results and previous actions.
Action followed by observation/feedback, with replanning when conditions change or an action fails.
Verification of the final outcome against objective constraints or evaluators.
A failure, conflict, or changed-condition scenario must be demonstrable during judging.
Architecture is open: participants may use one agent or multiple agents. Agent count is not a scoring criterion.
Track 1: Healthcare
Problem Statement 1: Autonomous Clinical Documentation & Follow-up Agent
Build an autonomous clinical documentation agent that converts a consultation into a verified follow-up record while resolving inconsistencies across multiple patient information sources.
The system receives a simulated consultation transcript together with previous notes, medication history, allergies, and laboratory reports. It must determine what information is relevant, reconcile conflicting facts, retrieve supporting information when required, draft structured documentation, verify the result, and flag consequential uncertainty for human review.

Required workflow:
• Ingest and reconcile information from multiple records.
• Identify missing, contradictory, or ambiguous facts.
• Retrieve relevant clinical knowledge or record evidence using provided tools.
• Draft a structured follow-up record and action list.
• Run consistency/validation checks.
• Revise the record or escalate unresolved conflicts.
• Demonstrate adaptation when a source contains conflicting or newly updated information.
Suggested sandbox tools: synthetic patient database, medication/allergy lookup, laboratory retrieval, clinical-guideline RAG, record-validation endpoint.
Guardrail: Use synthetic/deidentified data only. The system must not autonomously diagnose, prescribe, or make consequential clinical decisions.


Problem Statement 2: Adaptive Emergency Triage Agent
Build an autonomous patient-triage agent that determines the safest next routing decision while minimizing unnecessary questioning.
The agent begins with incomplete patient information and must conduct an adaptive interview. Each answer can change which information is needed next. It must combine symptoms and vital signs with a deterministic risk-scoring tool, maintain patient state, decide the appropriate routing action, and react when new or contradictory information appears.

Required workflow:
• Start with an incomplete patient state.
• Select the next question based on current uncertainty/risk.
• Query provided risk and patient-data tools.
• Update the patient state and risk assessment.
• Decide among predefined routing outcomes.
• Reassess when a new symptom/vital or contradictory answer appears.
• Escalate unresolved high-risk cases rather than inventing certainty.

Suggested sandbox tools: synthetic patient cases, risk-scoring algorithm, vitals/symptom database, optional clinical RAG.
Guardrail: This is decision support for a simulated environment, not medical diagnosis.

Track 2: Education
Problem Statement 3: Autonomous Learning Planner
Build an autonomous learning-planning agent that continuously works toward a student's learning goal under changing performance, availability, and resource constraints.
The system must not merely generate a study timetable. It should inspect performance data, identify knowledge gaps, select appropriate resources, schedule actions, observe completion/performance, and replan when the student misses sessions, improves faster than expected, or loses available study time.

Required workflow:
• Analyze current performance and identify priority gaps.
• Retrieve and select suitable learning resources.
• Create a schedule around calendar constraints.
• Track completed, missed, and newly available learning activities.
• Reassess progress.
• Replan future activities when constraints or performance change.
• Verify that the revised plan still satisfies time and learning objectives.

Suggested sandbox tools: synthetic LMS/performance API, educational RAG, calendar API, question bank, student-state store.


Problem Statement 4: Autonomous Assignment Review & Socratic Tutor
Build an autonomous assignment-review agent that helps a student correct multi-step work without directly revealing the final answer.
The system receives handwritten mathematics, diagrams, or code and must locate candidate errors, verify them with appropriate tools, decide the smallest useful intervention, observe the student's response, and adapt the level of guidance until the student reaches a correct solution or the system escalates.

Required workflow:
• Parse multimodal student work.
• Identify and verify a suspected error using a symbolic calculator, code sandbox, or reference.
• Select an appropriate hint rather than automatically providing the solution.
• Maintain conversational and assignment state.
• Reassess the student's next attempt.
• Escalate or change the hint strategy if the student remains stuck.
• Verify the final corrected work.

Suggested tools: Multimodal parser, symbolic calculator, code sandbox, rubric/reference knowledge base.
The key requirement is closed-loop tutoring and verification; a single multimodal LLM response is insufficient.


Track 3: Smart Automation
Problem Statement 5: Autonomous Customer Resolution Agent
Build an autonomous customer-resolution agent whose objective is to actually resolve a customer's issue across simulated enterprise systems, rather than merely classify the ticket or generate a reply.
The agent should inspect customer/order/policy information, decide an appropriate resolution, execute state-changing actions, verify their effects, and replan when an action is blocked or a new constraint appears.

Required workflow:
• Understand the customer's goal and current case state.
• Retrieve customer, order, inventory, and policy information.
• Select a resolution based on available evidence and constraints.
• Execute a simulated refund, replacement, cancellation, or other permitted action.
• Verify the state change.
• Adapt if inventory, policy, or another system prevents the original plan.
• Escalate only when the system cannot safely complete the objective.

Suggested sandbox tools: customer DB, order API, inventory API, refund/replacement/cancellation endpoints, policy RAG, verification endpoint.

Problem Statement 6: Autonomous Retail Supply Chain Recovery Agent
Build an autonomous supply-chain recovery agent that maintains service objectives when inventory, shipment, vendor, or demand conditions change.
The system must monitor a simulated logistics environment, detect disruptions, investigate alternatives, optimize under cost/delivery/carbon constraints, execute a recovery action, verify its outcome, and respond to a subsequent disruption.

Required workflow:
• Monitor inventory and shipment state.
• Detecting a disruption or constraint violation.
• Investigate alternative vendors/routes/allocations.
• Use optimization tools to compare feasible actions.
• Execute a simulated rerouting, purchase, allocation, or transfer.
• Verify the resulting inventory and delivery state.
• Replan when the chosen alternative becomes unavailable or another disruption occurs.
Suggested sandbox tools: inventory API, shipment/vendor APIs, route data, cost/carbon calculator, state-changing logistics endpoints.
Track 4: Sports
Problem Statement 7: Autonomous Fantasy Sports Manager
Build an autonomous fantasy-cricket manager that pursues a user's team objective under budget, squad, availability, and changing match-context constraints.
The agent must build a team using player data and contextual information, evaluate it with a scoring simulator, monitor changing conditions, and autonomously make justified changes when a player becomes unavailable or the context changes.

Required workflow:
• Interpret user preferences and constraints.
• Retrieve player statistics and contextual data.
• Generate candidate teams using a provided scoring/optimization tool.
• Validate budget and squad constraints.
• Evaluate the candidate in a simulated fantasy environment.
• React to injury/availability/news/weather changes by re-querying tools and rebuilding the relevant parts of the team.
• Optionally execute create/swap/submit actions through a simulated fantasy platform.
• Verify that the final team satisfies all constraints.

Suggested sandbox tools: player statistics API, simulated weather/news/availability feeds, fantasy scoring simulator, simulated create/swap/submit API.
No real-money betting or real-world account actions are required.

Problem Statement 8: Autonomous Athlete Performance Planner
Build an autonomous athlete-performance planning agent that maintains a training objective under changing workload, recovery, and schedule constraints.
The system receives synthetic GPS/workload, recovery, wellness, and match-schedule data. It must create a plan, monitor updated state, decide how the next training actions should change, and verify that workload constraints remain satisfied.

Required workflow:
• Assess current workload, recovery, and upcoming competition demands.
• Create a training plan using a provided load-management algorithm.
• Schedule concrete training actions.
• Observe updated workload/recovery data.
• Recalculate the plan when fatigue, availability, or match schedule changes.
• Demonstrate at least two meaningful plan revisions.
• Verify the final plan against workload and scheduling constraints.

Suggested sandbox tools: synthetic GPS/workload API, wellness/recovery data, match calendar, load-management calculator.
Guardrail: Do not make medical diagnoses or injury-treatment claims; the environment is for performance-planning research.
Track 5: Cybersecurity
Problem Statement 9: Autonomous SOC Investigation & Response Agent
Build an autonomous SOC agent that investigates security alerts to determine whether an attack actually succeeded and performs an appropriate simulated response.
The system must correlate alerts with asset, vulnerability, configuration, and response evidence rather than relying on the alert label alone. It must decide what evidence to retrieve next, determine the attack outcome, take a sandboxed response action where appropriate, verify the effect, and reconsider its conclusion when new evidence appears.

Required workflow:
• Ingest simulated NIDS/Snort/Suricata alerts.
• Retrieve packet metadata, asset information, vulnerabilities, and server logs.
• Determine what additional evidence is needed.
• Establish whether the attack succeeded or failed.
• Generate an evidence-backed incident assessment.
• Execute a simulated firewall/block action when justified.
• Re-check the environment after the action and adapt to feedback or human override.

Suggested sandbox tools: simulated NIDS alerts, packet/server logs, asset inventory, synthetic CVE KB, simulated firewall.
All actions must remain inside the provided sandbox.


Problem Statement 10: Autonomous Cloud IAM Least-Privilege Mitigator
Build an autonomous cloud-IAM agent that reduces excessive permissions without breaking simulated service dependencies.
The agent must inspect IAM assignments and access history, identify candidate permissions for removal, simulate the impact of proposed changes, reason over failures or dependency information, revise the policy, and verify that the revised policy preserves required access.

Required workflow:
• Analyze IAM roles, access logs, and service dependencies.
• Identify suspicious or unused permissions.
• Propose a least-privilege policy.
• Simulate its rollout and inspect impact.
• If a required service fails, identify the dependency and revise the policy.
• Re-simulate until the policy satisfies both security and functionality constraints.
• Produce the final policy and evidence supporting each change.
Suggested sandbox tools: Audit-log parser, IAM policy simulator, service dependency graph, synthetic cloud environment.
No production credentials or real cloud changes are required.

Track 6: Career & Applications
Problem Statement 11: Autonomous Resume & Application Agent
Build an autonomous application-preparation agent that takes a candidate's base information and a target role and works toward a strong, truthful, role-specific application.
The system must independently determine the information and actions needed to tailor the application. It should research the target role, inspect candidate evidence, draft and render the resume, evaluate it, identify weaknesses, revise it, and verify factual consistency.

Required workflow:
• Parse the target job description and identify relevant requirements.
• Research the role/company using provided search or knowledge tools.
• Inspect the candidate's resume, project/profile evidence, and available supporting material.
• Decide which genuine evidence is relevant to the target role.
• Produce a tailored resume and render it as a PDF.
• Run ATS/relevance, formatting, and factual-consistency evaluation.
• Replan and revise when evaluation reveals weaknesses or unsupported claims.
• Verify the final application package before delivery.
• Produce an evidence/change report explaining why important edits were made.
Suggested sandbox tools: JD parser, company/role research source or supplied KB, candidate-profile/project repository, PDF renderer, ATS evaluator, factual-consistency checker.
Guardrail: The system must never fabricate skills, projects, credentials, employment, or achievements.
Submission Requirements
Presentation summary: It should be able to explain the approach, final solution, challenges and your conclusion.
Demo video: It must show Goal → Decision → Action → Intermediate Result → Adaptation → Final Outcome.
Source code/ GitHub repository 
A runnable version of your solution (not necessary but encouraged if applicable).

A one-shot LLM answer, simple RAG system, static ML model, or fixed prompt chain without meaningful autonomous action and adaptation won't qualify as an Agentic AI solution.
Participants may use one agent or multiple agents. The number of agents, frontend, backend, or framework choice should not itself earn points.
Evaluation Rubric

Criterion
Weight


Agentic workflow & autonomy
25%
Tool/environment interaction
15%
Adaptation & failure recovery
15%
Technical implementation
15%
Problem relevance & innovation
10%
Prototype functionality & UX
10%
Evaluation, verification & robustness
10%




[For the submission we request all the participants to submit their files with their ’Team name_Github/Agentic’ type format.]

For example: If your team name is ‘Tech rebels’ -> submission for the demo video will be: ‘Techrebels_video_agentic’

