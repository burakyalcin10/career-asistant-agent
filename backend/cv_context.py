"""
CV/Profile Context Module
Provides Burak Yalçın's professional profile information as context for the Career Agent.
"""

CV_CONTEXT = """
=== CANDIDATE PROFILE ===

Name: Burak YALÇIN
Title: Computer Engineering Student & Part-Time Software Engineer
Email: burakyalcin.4510@gmail.com
Phone: +90 507 083 37 94
Location: Antalya, Turkey
LinkedIn: linkedin.com/in/burakyalcin
GitHub: github.com/burakyalcin
Birth Year: 2002

=== SUMMARY ===
Computer Engineering student at Akdeniz University (GPA: 3.39), passionate about AI, Software Engineering, 
and Full-Stack Development. Currently working as a Part-Time Software Engineer at SAN TSG, a leading tourism 
technology company. Chairman of the Board of Directors at Akdeniz University's Software, AI and Creativity 
Community (3Y). In free time, enjoys writing poetry and practicing traditional dance.

=== EDUCATION ===
- Akdeniz University, Antalya, Turkey (2022 – present)
  Bachelor's Degree in Computer Science & Engineering
  GPA: 3.39

=== PROFESSIONAL EXPERIENCE ===

1. Part-Time Software Engineer, SAN TSG (October 2025 – Present)
   - Continuing development of AI-driven solutions and backend services
   - Focus on scalability and performance optimizations
   - Maintaining and enhancing RESTful APIs using Python and FastAPI
   - Tech Stack: Python, LangChain, Pinecone, FastAPI, Streamlit

2. Software Engineering Intern, SAN TSG (July 2025 – August 2025)
   - Developed AI-powered RAG system for natural language API documentation queries
   - Led sprint cycles as Scrum Master, ensuring on-time project delivery
   - Built robust APIs with FastAPI and integrated vector databases
   - Tech Stack: Python, LangChain, Pinecone, FastAPI, Streamlit

3. Educator & Mentor, T3 Foundation (February 2024 – Present)
   - Mentored 50+ high school students in STEM-oriented projects
   - Enhanced problem-solving and analytical thinking skills

=== KEY PROJECTS ===

1. AI-Powered RAG System for API Documentation
   - Built natural language API documentation query system
   - Tech: Python, LangChain, Pinecone, FastAPI, Streamlit
   - Live: http://docs-ai.santsg.com/

2. TÜBİTAK 2209-A: Smart Irrigation System (Agrotopia)
   - IoT-based smart irrigation using Raspberry Pi and Arduino sensors
   - AI algorithms to optimize water usage (improved crop health by 30%)
   - Project Coordinator role

3. E-Commerce Platform with AI Features
   - Full-stack: Angular frontend + Spring Boot backend + MySQL
   - AI-powered product recommendations
   - GitHub: github.com/agrotopya/ecommerce_with_angular_springboot_mysql

4. AI-Powered Lyrics Synchronization Player
   - Python app with OpenAI Whisper for real-time lyrics display
   - VLC media player API integration
   - GitHub: github.com/burakyalcin10/SarkiSozleriPlayer

5. Combinatorial Article on Fibonacci and Catalan Paths (December 2025)
   - Academic paper on lattice paths with Fibonacci, Catalan, and Motzkin numbers
   - Python-based algorithms and visualization techniques

=== TECHNICAL SKILLS ===
- Languages: Python, Java, C#, TypeScript, HTML, CSS
- Frameworks: FastAPI, Spring Boot, Angular, Flask, Streamlit
- AI/ML: LangChain, Pinecone, OpenAI, RAG Systems
- Tools: Git, Docker, Raspberry Pi, Arduino
- Languages Spoken: Turkish (Native), English (Proficient)

=== LEADERSHIP & ORGANIZATIONS ===
- Chairman of Board of Directors, Akdeniz Yazılım, Yapay Zeka ve Yaratıcılık (3Y) Community (2023 – present)
  - Founded and leads community organizing AI and software development training for 100+ students
  - Co-organized DevFest Antalya 2025 with GDG Antalya
- Vice President, BİLMÖK Organizing Committee (May 2024 – Feb 2025)
  - Coordinated 21st National Informatics Congress for 500+ participants
- Organization Officer, UBMK24 Conference
- Volunteer, TEKNOFEST 2025

=== CERTIFICATES ===
- UBMK 2024
- Erasmus+ KA 154
- TÜBİTAK 2209A
- 42 Hour Java

=== REFERENCES ===
- Prof. Dr. Ümit Deniz ULUŞAR, Chair, Dept. of Computer Engineering, Akdeniz University
- Alper ÖZEN, Software Development Manager, SAN TSG
- Furkan ÜNSAL, Human Resources Specialist, TÜBİTAK

=== AVAILABILITY ===
- Available for internships, part-time, and full-time positions
- Preferred areas: AI/ML, Backend Development, Full-Stack Development
- Open to remote and on-site opportunities in Turkey and abroad

=== INSTRUCTIONS FOR THE AGENT ===
When responding on behalf of Burak:
- Always maintain a professional, polite, and enthusiastic tone
- Highlight relevant experience and projects based on the employer's query
- Be honest about skills and experience levels
- Express genuine interest in learning opportunities
- Never make false claims about skills or experience not listed above
- For salary discussions, politely defer to direct conversation with Burak
- For legal questions, redirect to Burak for direct handling
"""

def get_cv_context() -> str:
    """Returns the full CV context string."""
    return CV_CONTEXT
