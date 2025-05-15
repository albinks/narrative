"""
LLM Renderer

This module contains the LLMRenderer class, which renders trajectories into natural language
stories using large language models (LLMs).
"""

from typing import Dict, List, Any, Optional, Protocol
from abc import ABC, abstractmethod

from narrative.core.trajectory_explorer import Trajectory


class LLMAdapter(ABC):
    """
    Abstract base class for LLM adapters.
    
    An LLM adapter is responsible for communicating with a specific LLM API or service.
    """
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate text from a prompt using an LLM.
        
        Args:
            prompt: The prompt to send to the LLM.
            
        Returns:
            The generated text.
        """
        pass


class MockLLMAdapter(LLMAdapter):
    """
    A mock LLM adapter that returns a predefined response.
    
    This adapter is useful for testing and development when you don't want to make
    actual API calls to an LLM service.
    """
    
    def generate(self, prompt: str) -> str:
        """
        Generate text from a prompt using a mock LLM.
        
        Args:
            prompt: The prompt to send to the mock LLM.
            
        Returns:
            A predefined response.
        """
        return """
Once upon a time, there was a little girl named Little Red Riding Hood. She was called that because she always wore a red hooded cloak that her grandmother had made for her.

One day, Little Red Riding Hood's mother asked her to take a basket of food to her grandmother, who lived in a cottage in the forest. The grandmother had been feeling ill, and the food would help her feel better.

"Remember, go straight to Grandmother's house," her mother warned. "Don't talk to strangers and don't wander off the path."

Little Red Riding Hood promised to be careful and set off into the forest. As she walked along the path, she met a wolf. The wolf was cunning and wicked, and when he saw the little girl, he immediately began to think about how he could catch and eat her.

"Good day, Little Red Riding Hood," said the wolf, trying to sound friendly.

"Good day, Mr. Wolf," she replied, not knowing that he was dangerous.

"Where are you going on this fine morning?" asked the wolf.

"I'm going to visit my grandmother. She's ill, and I'm taking her some food," Little Red Riding Hood answered.

The wolf thought quickly. "Where does your grandmother live?" he asked.

"In a cottage in the forest, just beyond the old oak tree," said Little Red Riding Hood, pointing down the path.

The wolf smiled wickedly. "I hope your grandmother feels better soon," he said, and then he hurried away.

The wolf ran ahead to the grandmother's cottage and knocked on the door.

"Who is it?" called the grandmother from inside.

"It's Little Red Riding Hood," the wolf said, disguising his voice. "I've brought you some food."

The grandmother, who was in bed, called out, "Pull the string, and the latch will open."

The wolf pulled the string, opened the door, and without saying another word, he swallowed the grandmother whole. Then he put on her nightcap and nightgown and got into her bed, pulling the covers up to his nose.

Soon, Little Red Riding Hood arrived at the cottage and knocked on the door.

"Who is it?" called the wolf, trying to sound like the grandmother.

"It's Little Red Riding Hood. I've brought you some food," she replied.

"Pull the string, and the latch will open," said the wolf.

Little Red Riding Hood pulled the string, opened the door, and went inside. She was surprised to see how different her grandmother looked.

"Grandmother, what big eyes you have!" she exclaimed.

"All the better to see you with, my dear," replied the wolf.

"Grandmother, what big ears you have!"

"All the better to hear you with, my dear."

"Grandmother, what big teeth you have!"

"All the better to eat you with!" growled the wolf, and he leaped out of bed and swallowed Little Red Riding Hood whole, just as he had done with her grandmother.

Feeling satisfied, the wolf climbed back into bed and fell asleep, snoring loudly.

A hunter who was passing by the cottage heard the loud snoring and thought it strange that the old woman would snore so loudly. He decided to check if everything was alright.

When the hunter entered the cottage, he saw the wolf lying in the bed, still wearing the grandmother's nightcap.

"So I've found you at last, you old sinner!" said the hunter. "I've been looking for you for a long time!"

The hunter was about to shoot the wolf when he thought that the wolf might have eaten the grandmother. Instead of shooting, he took a pair of scissors and cut open the wolf's belly.

To his surprise, out jumped Little Red Riding Hood and her grandmother, both alive and well.

"Thank you, kind hunter," they said gratefully.

Little Red Riding Hood quickly gathered some heavy stones, and they filled the wolf's belly with them while he was still asleep. When the wolf woke up, he tried to run away, but the stones were so heavy that he collapsed and died.

The hunter took the wolf's pelt, the grandmother enjoyed the food that Little Red Riding Hood had brought, and Little Red Riding Hood promised herself never to talk to strangers in the forest again.

And they all lived happily ever after.
"""


class OpenAIAdapter(LLMAdapter):
    """
    An adapter for the OpenAI API.
    
    This adapter uses the OpenAI API to generate text from prompts.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize an OpenAIAdapter.
        
        Args:
            api_key: The OpenAI API key.
            model: The model to use (default: "gpt-4").
        """
        try:
            import openai
        except ImportError:
            raise ImportError(
                "OpenAI is required for this adapter. "
                "Install it with 'pip install openai'."
            )
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str) -> str:
        """
        Generate text from a prompt using the OpenAI API.
        
        Args:
            prompt: The prompt to send to the OpenAI API.
            
        Returns:
            The generated text.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        
        return response.choices[0].message.content


class LLMRenderer:
    """
    Renderer class for converting trajectories into natural language stories using LLMs.
    """
    
    def __init__(self, adapter: Optional[LLMAdapter] = None):
        """
        Initialize an LLMRenderer.
        
        Args:
            adapter: The LLM adapter to use. If not provided, a MockLLMAdapter will be used.
        """
        self.adapter = adapter or MockLLMAdapter()
    
    def render(self, trajectory: Trajectory) -> str:
        """
        Render a trajectory into a natural language story.
        
        Args:
            trajectory: The trajectory to render.
            
        Returns:
            A natural language story.
        """
        prompt = self._create_prompt(trajectory)
        response = self.adapter.generate(prompt)
        return self._process_response(response)
    
    def _create_prompt(self, trajectory: Trajectory) -> str:
        """
        Create a prompt for the LLM from a trajectory.
        
        Args:
            trajectory: The trajectory to create a prompt from.
            
        Returns:
            A prompt for the LLM.
        """
        prompt = "Create a coherent and engaging story based on the following sequence of intentions:\n\n"
        
        for i, intention in enumerate(trajectory.intentions):
            prompt += f"{i+1}. {intention['character']} intends to {intention['id']} {intention['target']} at {intention['location']}"
            
            if intention.get("description"):
                prompt += f" {intention['description']}"
            
            prompt += "\n"
        
        prompt += "\nThe story should follow this sequence of intentions, but feel free to add details, dialogue, and descriptions to make it engaging. The story should be coherent and flow naturally from one intention to the next."
        
        return prompt
    
    def _process_response(self, response: str) -> str:
        """
        Process the response from the LLM.
        
        Args:
            response: The response from the LLM.
            
        Returns:
            The processed response.
        """
        # For now, just return the response as is
        return response
