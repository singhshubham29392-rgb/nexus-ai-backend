class TaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class AIConfig:
    DEFAULT_PROMPT_PREFIX = "As the Nexus AI Project Manager, please analyze the following requirement: "
    MAX_OUTPUT_TOKENS = 1000
    TEMPERATURE = 0.7