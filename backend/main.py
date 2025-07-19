#!/usr/bin/env python3
"""
CompetitorCrusher - AI-Powered Competitive Intelligence Engine
Backend for PDF processing and deep research analysis
"""

import os
import json
import requests
from datetime import datetime
import PyPDF2
from io import BytesIO
import time
from typing import Dict, List, Optional
import os

from backend.config import PERPLEXITY_API_KEY, check_api_key

class CompetitorAnalyzer:
    def __init__(self, perplexity_api_key: str):
        self.perplexity_key = perplexity_api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
        
    def extract_pdf_content(self, pdf_file_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            with open(pdf_file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract PDF content: {str(e)}")
    
    def extract_company_name(self, content: str) -> str:
        """Extract company name from PDF content"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Try first line if it's short (likely company name)
        if lines and len(lines[0]) < 100:
            first_line = lines[0]
            # Clean up the line
            company_name = ''.join(c for c in first_line if c.isalnum() or c.isspace()).strip()
            if company_name:
                return company_name
        
        # Look for "Company:" patterns
        for line in lines[:10]:  # Check first 10 lines
            if any(keyword in line.lower() for keyword in ['company:', 'name:', 'about']):
                parts = line.split(':')
                if len(parts) > 1:
                    return parts[1].strip()
        
        return "Unknown Company"
    
    def research_with_perplexity(self, query: str, context: str = "") -> Dict:
        """Make API call to Perplexity for deep research"""
        headers = {
            'Authorization': f'Bearer {self.perplexity_key}',
            'Content-Type': 'application/json'
        }
        
        full_query = f"{context}\n\n{query}" if context else query
        
        system_prompt = """You are an expert competitive intelligence analyst. 
Provide detailed, actionable insights with specific examples, numbers, and data points. 
Always cite your sources and include URLs when available.
Focus on practical business intelligence that can drive strategic decisions.
Be comprehensive but concise."""
        
        final_prompt = f"{system_prompt}\n\n{full_query}"

        payload = {
            "model": "sonar-deep-research",
            "messages": [
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=None)
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and result['choices']:
                content = result['choices'][0]['message']['content']
                return {
                    'analysis': content,
                    'sources': self._extract_sources(content),
                    'timestamp': datetime.now().isoformat(),
                    'success': True
                }
            else:
                return {
                    'error': 'No response from API',
                    'raw_response': result,
                    'success': False
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'error': f'API request failed: {str(e)}',
                'success': False
            }
        except Exception as e:
            return {
                'error': f'Analysis failed: {str(e)}',
                'success': False
            }
    
    def _extract_sources(self, content: str) -> Dict:
        """Extract URLs and citations from response"""
        import re
        
        # Find URLs
        url_pattern = r'https?://[^\s\)\]\}]+'
        urls = re.findall(url_pattern, content)
        
        # Find citations in brackets
        citation_pattern = r'\[[^\]]+\]'
        citations = re.findall(citation_pattern, content)
        
        return {
            'urls': list(set(urls)),  # Remove duplicates
            'citations': list(set(citations)),
            'total_sources': len(set(urls + citations))
        }
    
    def analyze_competitors(self, company_data: str, company_name: str) -> Dict:
        """
        Perform comprehensive competitor analysis based on company data
        """
        print(f"🔍 Starting competitor analysis for: {company_name}")
        
        # Context for all queries
        context = f"""
COMPANY PROFILE FOR {company_name}:
{company_data[:2000]}

Based on this company profile, research and analyze the competitive landscape.
"""
        
        analysis_results = {
            'company_name': company_name,
            'timestamp': datetime.now().isoformat(),
            'analysis_sections': {}
        }
        
        # 1. Competitor Identification
        print("📊 1/7 Identifying competitors...")
        competitors_query = f"""
Find the TOP 5 DIRECT competitors and TOP 3 INDIRECT competitors for {company_name}.
Also identify:
- 3 emerging startups in this space
- 2 big tech companies that might enter this market
- Alternative solutions customers might choose instead

For each competitor, provide:
- Company name and brief description
- Why they're a threat to {company_name}
- Market position and recent funding/developments
- Key differentiators

Include specific sources and recent data.
"""
        analysis_results['analysis_sections']['competitors'] = self.research_with_perplexity(competitors_query, context)
        time.sleep(2)  # Rate limiting
        
        # 2. Products & Services Analysis
        print("🛠️ 2/7 Analyzing products & services...")
        products_query = f"""
Research and compare {company_name}'s products/services with their top competitors:

- Detailed feature-by-feature comparison with top 3 competitors
- What unique features do competitors have that {company_name} lacks?
- What's in competitors' product roadmaps and development pipelines?
- Recent product launches and innovations by competitors
- Technical capabilities and specifications comparison
- Customer reviews comparing products

Provide specific examples, feature lists, and performance comparisons.
"""
        analysis_results['analysis_sections']['products'] = self.research_with_perplexity(products_query, context)
        time.sleep(2)
        
        # 3. Pricing Strategy Analysis
        print("💰 3/7 Researching pricing strategies...")
        pricing_query = f"""
Research detailed pricing strategies for {company_name} and their competitors:

- Exact pricing tiers and models for top 5 competitors
- Subscription vs usage-based vs one-time pricing models
- Enterprise vs SMB pricing differences
- Discounts, promotions, and loyalty programs
- How customers perceive value vs price (review analysis)
- Estimated profit margins and cost structures
- Recent pricing changes and market reactions

Include specific pricing examples with sources.
"""
        analysis_results['analysis_sections']['pricing'] = self.research_with_perplexity(pricing_query, context)
        time.sleep(2)
        
        # 4. Marketing & Sales Strategy
        print("📢 4/7 Analyzing marketing & sales...")
        marketing_query = f"""
Analyze marketing and sales strategies for {company_name}'s main competitors:

- Target audience demographics, psychographics, and personas
- Brand positioning and messaging strategies
- Marketing channels: paid ads, content marketing, social media, partnerships
- Content marketing performance: blog topics, video strategies, case studies
- SEO strategy: keywords they rank for, content gaps
- Sales processes: lead generation, sales funnels, conversion tactics
- Recent successful marketing campaigns and their results

Provide specific campaign examples and performance metrics.
"""
        analysis_results['analysis_sections']['marketing'] = self.research_with_perplexity(marketing_query, context)
        time.sleep(2)
        
        # 5. Customer Experience & Sentiment
        print("😊 5/7 Evaluating customer experience...")
        customer_query = f"""
Research customer experience and sentiment for {company_name}'s competitors:

- Customer service quality: support channels, response times, satisfaction ratings
- User onboarding and customer journey analysis
- Customer reviews analysis: common complaints and praise
- Customer retention rates and loyalty metrics
- User experience strengths and weaknesses
- Support documentation and community engagement
- Customer success stories and case studies

Include review excerpts and sentiment analysis data.
"""
        analysis_results['analysis_sections']['customer_experience'] = self.research_with_perplexity(customer_query, context)
        time.sleep(2)
        
        # 6. Business Operations & Financial Health
        print("🏭 6/7 Assessing business operations...")
        operations_query = f"""
Research business operations and financial health of {company_name}'s competitors:

- Company sizes: employee counts, office locations, remote work policies
- Market share estimates and revenue data
- Recent funding rounds, valuations, and investor information
- Technology stacks and infrastructure choices
- Partnership strategies and distribution channels
- Operational efficiency indicators and business model analysis
- Growth metrics, expansion plans, and hiring trends

Include financial data and operational benchmarks.
"""
        analysis_results['analysis_sections']['business_operations'] = self.research_with_perplexity(operations_query, context)
        time.sleep(2)
        
        # 7. SWOT Analysis
        print("⚡ 7/7 Performing SWOT analysis...")
        swot_query = f"""
Perform a comprehensive SWOT analysis for {company_name} versus their competitive landscape:

STRENGTHS:
- What does {company_name} do better than competitors?
- Unique advantages and competitive moats
- Strong points in their market positioning

WEAKNESSES:
- Where do competitors clearly outperform {company_name}?
- Missing features, capabilities, or market presence
- Areas needing immediate improvement

OPPORTUNITIES:
- Market gaps {company_name} could exploit
- Competitor weaknesses they could capitalize on
- Emerging trends they could lead or leverage

THREATS:
- Biggest competitive threats and their strategies
- Market shifts that could hurt {company_name}
- Competitor moves to watch out for

Be specific with examples and actionable recommendations.
"""
        analysis_results['analysis_sections']['swot'] = self.research_with_perplexity(swot_query, context)
        
        print("✅ Analysis complete!")
        return analysis_results
    
    def save_analysis_report(self, analysis_results: Dict, output_file: str = None) -> str:
        """Save analysis results to JSON file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            company_name = analysis_results.get('company_name', 'unknown').replace(' ', '_')
            output_file = f"competitor_analysis_{company_name}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        return output_file

def main():
    """Main function to run the competitor analysis"""
    
    # Configuration
    if not check_api_key():
        return
        
    # Get company data file from user
    default_file = 'company_data.txt'
    file_path = input(f"📄 Enter the path to your company data file (or press Enter for '{default_file}'): ").strip()
    
    if not file_path:
        file_path = default_file
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            company_data = f.read()
    except FileNotFoundError:
        print(f"❌ Error: The file '{file_path}' was not found.")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
        
    # Initialize analyzer
    analyzer = CompetitorAnalyzer(PERPLEXITY_API_KEY)
    
    # Extract company name from content
    company_name = analyzer.extract_company_name(company_data)
    print(f"🏢 Detected company: {company_name}")
    
    # Perform analysis
    print(f"\n🚀 Starting comprehensive competitive analysis...")
    print(f"⏱️  This may take several minutes depending on the analysis depth...\n")
    
    try:
        results = analyzer.analyze_competitors(company_data, company_name)
        
        # Save results
        output_file = analyzer.save_analysis_report(results)
        print(f"\n📄 Analysis saved to: {output_file}")
        
        # Print summary
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"Company: {results['company_name']}")
        print(f"Completed: {results['timestamp']}")
        print(f"Sections analyzed: {len(results['analysis_sections'])}")
        
        for section, data in results['analysis_sections'].items():
            if data.get('success'):
                source_count = data.get('sources', {}).get('total_sources', 0)
                print(f"✅ {section.replace('_', ' ').title()}: {source_count} sources")
            else:
                print(f"❌ {section.replace('_', ' ').title()}: Failed - {data.get('error', 'Unknown error')}")
        
        return results
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        return None

if __name__ == "__main__":
    main()