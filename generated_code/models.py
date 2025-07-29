class Agent:
    """Represents an Agent in the system."""
    def __init__(self, agent_id, name, email):
        self.agent_id = agent_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Agent(agent_id={self.agent_id}, name={self.name}, email={self.email})"

class Task:
    """Represents a Task in the system."""
    def __init__(self, task_id, title, description, status='pending', assigned_agent_id=None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.assigned_agent_id = assigned_agent_id

    def __repr__(self):
        return f"Task(task_id={self.task_id}, title={self.title}, status={self.status})"