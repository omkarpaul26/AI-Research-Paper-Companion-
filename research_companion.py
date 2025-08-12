# Simplified AI Research Paper Companion - No crewai-tools required
# This version works without external tool dependencies

import os
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import requests

print("🚀 Starting AI Research Paper Companion...")

# Set your OpenAI API key (already in your code)
os.environ["OPENAI_API_KEY"] = "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"

# Initialize the language model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)  # Using cheaper model first
print("✅ Language model initialized")

class ResearchPaperCompanion:
    def __init__(self):
        print("🔧 Setting up research agents...")
        self.setup_agents()
    
    def setup_agents(self):
        """Initialize the three specialized agents"""
        
        # Agent 1: Topic Explainer
        self.topic_explainer = Agent(
            role="Research Topic Explainer",
            goal="Break down complex research topics into understandable components and provide comprehensive explanations",
            backstory="""You are an expert academic researcher with a PhD in multiple disciplines. 
            You excel at taking complex research topics and breaking them down into digestible pieces.
            You can explain technical concepts clearly, identify key terminology, and provide context 
            about how topics fit into broader research landscapes.""",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        print("✅ Topic Explainer agent created")
        
        # Agent 2: Literature Finder
        self.literature_finder = Agent(
            role="Academic Literature Researcher",
            goal="Find, evaluate, and summarize relevant academic papers and research materials",
            backstory="""You are a skilled research librarian and academic researcher with expertise 
            in finding high-quality academic sources. You know how to search academic databases, 
            evaluate paper quality, identify seminal works, and find recent developments in any field.
            You're excellent at determining which papers are most relevant and impactful.""",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        print("✅ Literature Finder agent created")
        
        # Agent 3: Gap Analyzer
        self.gap_analyzer = Agent(
            role="Research Gap Analyst",
            goal="Identify research gaps, limitations, and future research directions from literature analysis",
            backstory="""You are a senior research strategist with extensive experience in identifying 
            research opportunities. You excel at analyzing existing literature to find what's missing, 
            what questions remain unanswered, and what methodological improvements could be made. 
            You're skilled at synthesizing findings and suggesting novel research directions.""",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        print("✅ Gap Analyzer agent created")
    
    def create_tasks(self, research_topic):
        """Create dynamic tasks based on the research topic"""
        
        # Task 1: Explain the Research Topic
        topic_explanation_task = Task(
            description=f"""
            Analyze and explain the research topic: "{research_topic}"
            
            Your task is to:
            1. Break down the topic into key components and concepts
            2. Explain technical terminology in accessible language
            3. Provide background context and historical development
            4. Identify the main research areas and subdisciplines involved
            5. Explain why this topic is important and relevant
            6. Identify key researchers, institutions, or landmark studies in this area
            
            Provide a comprehensive yet accessible explanation that would help someone 
            new to the field understand the topic thoroughly.
            """,
            agent=self.topic_explainer,
            expected_output="A detailed explanation document with clear sections covering all requested aspects of the research topic"
        )
        
        # Task 2: Find and Summarize Literature (using agent's knowledge)
        literature_search_task = Task(
            description=f"""
            Based on your knowledge, provide an analysis of relevant academic literature for: "{research_topic}"
            
            Your task is to:
            1. Identify 10-15 most important and influential papers in this field
            2. For each significant paper/study, provide:
               - Title and authors (if known)
               - Publication venue and approximate year
               - Key findings and contributions
               - Methodology approach
               - Impact on the field
            3. Categorize papers by subtopic or methodological approach
            4. Identify seminal/foundational works vs recent developments
            5. Note highly cited or breakthrough papers
            6. Discuss major research groups or institutions leading this field
            
            Focus on the most impactful academic sources and landmark studies.
            Use your knowledge of the field to provide authoritative information.
            """,
            agent=self.literature_finder,
            expected_output="A comprehensive literature review with categorized paper summaries and analysis",
            dependencies=[topic_explanation_task]
        )
        
        # Task 3: Analyze Research Gaps and Suggest Directions
        gap_analysis_task = Task(
            description=f"""
            Based on the topic explanation and literature review, identify research gaps and opportunities for: "{research_topic}"
            
            Your task is to:
            1. Analyze the current state of research in this field
            2. Identify gaps in knowledge, methodology, or application
            3. Note areas with conflicting findings or unresolved debates
            4. Identify underexplored subtopics, populations, or use cases
            5. Suggest methodological improvements or novel approaches
            6. Propose 5-7 specific research questions that could address these gaps
            7. Create a detailed research outline for a potential paper addressing one major gap
            8. Suggest potential collaboration opportunities or interdisciplinary approaches
            9. Identify practical applications or real-world implementations needed
            
            Be specific and actionable in your recommendations.
            Focus on feasible research directions that could make significant contributions.
            """,
            agent=self.gap_analyzer,
            expected_output="A detailed gap analysis with specific research recommendations and a sample research outline",
            dependencies=[topic_explanation_task, literature_search_task]
        )
        
        return [topic_explanation_task, literature_search_task, gap_analysis_task]
    
    def analyze_research_topic(self, research_topic):
        """Main method to analyze a research topic"""
        
        print(f"\n🔍 Starting analysis of research topic: {research_topic}")
        print("=" * 80)
        
        # Create tasks dynamically
        tasks = self.create_tasks(research_topic)
        
        # Create crew with the tasks
        crew = Crew(
            agents=[self.topic_explainer, self.literature_finder, self.gap_analyzer],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        print(f"\n🚀 Executing analysis with {len(tasks)} tasks...")
        
        # Execute the crew
        result = crew.kickoff()
        
        return result
    
    def save_results(self, results, output_file="research_analysis_output.md"):
        """Save the analysis results to a file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# AI Research Paper Companion Analysis\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(str(results))
        
        print(f"📄 Results saved to {output_file}")

# Main execution
if __name__ == "__main__":
    print("\n" + "="*80)
    print("🎯 AI RESEARCH PAPER COMPANION")
    print("="*80)
    
    # Initialize the research companion
    try:
        companion = ResearchPaperCompanion()
        print("✅ Research companion initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        exit(1)
    
    # Example research topics to analyze
    research_topics = [
        "Transformer architectures in natural language processing",
        "Federated learning for healthcare applications",
        "Explainable AI in financial decision making",
        "Graph neural networks for drug discovery",
        "Reinforcement learning for autonomous vehicle navigation"
    ]
    
    # Choose a topic or get user input
    print("\nAvailable research topics:")
    for i, topic in enumerate(research_topics, 1):
        print(f"{i}. {topic}")
    
    choice = input(f"\nEnter topic number (1-{len(research_topics)}) or type your own topic: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(research_topics):
        selected_topic = research_topics[int(choice) - 1]
    else:
        selected_topic = choice if choice else research_topics[0]
    
    print(f"\n📋 Selected topic: {selected_topic}")
    print("⏳ This analysis will take 3-5 minutes...")
    
    try:
        # Run the analysis
        results = companion.analyze_research_topic(selected_topic)
        
        # Save results
        companion.save_results(results)
        
        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print("📄 Check 'research_analysis_output.md' for detailed results.")
        print("=" * 80)
        
        # Show preview
        print("\n📖 Preview of results:")
        print("-" * 40)
        result_preview = str(results)[:500]
        print(result_preview + "...")
        print("-" * 40)
        print(f"💰 Estimated cost: ~$0.50-2.00 (using GPT-3.5-turbo)")
        
    except Exception as e:
        print(f"\n❌ Analysis failed: {str(e)}")
        print("💡 Common issues:")
        print("  - Check your OpenAI API key")
        print("  - Ensure you have sufficient OpenAI credits")
        print("  - Check your internet connection")
        
        # Import traceback for detailed error info
        import traceback
        print(f"\n🔍 Detailed error:")
        traceback.print_exc()

print("\n🏁 Program finished.")