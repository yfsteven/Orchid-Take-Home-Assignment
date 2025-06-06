import os
import json
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime

class LLMGenerator:
    """LLM integration for generating HTML clones"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY', '')
        self.model = "claude-3-sonnet-20240229"  # Recommended model
    
    async def generate_html(self, design_context: Dict[str, Any]) -> str:
        """Generate HTML based on scraped design context"""
        
        # Create a comprehensive prompt
        prompt = self._create_prompt(design_context)
        
        # For demo purposes, we'll use a sophisticated template generator
        # In production, replace this with actual Claude API call
        html = await self._generate_with_template(design_context)
        
        return html
    
    def _create_prompt(self, context: Dict[str, Any]) -> str:
        """Create a detailed prompt for the LLM"""
        prompt = f"""
You are an expert web developer tasked with creating an HTML clone of a website.
Based on the following design context, generate a complete, single-file HTML page that closely matches the original website's aesthetics.

DESIGN CONTEXT:
- URL: {context['url']}
- Title: {context['title']}
- Meta Description: {context['meta'].get('description', 'N/A')}
- Theme Color: {context['meta'].get('theme-color', '#000000')}

STRUCTURE:
- Has Header: {context['structure']['has_header']}
- Has Footer: {context['structure']['has_footer']}
- Has Sidebar: {context['structure']['has_sidebar']}
- Main Sections: {context['structure']['main_sections']}
- Layout Type: {context['layout']['layout_type']}

TYPOGRAPHY:
- Font Families: {', '.join(context['typography']['fonts'][:3]) if context['typography']['fonts'] else 'Default'}
- Font Sizes Used: {', '.join(context['typography']['font_sizes'][:5]) if context['typography']['font_sizes'] else 'Default'}

COLOR PALETTE:
- Background Colors: {', '.join(context['colors']['background'][:3]) if context['colors']['background'] else '#ffffff'}
- Text Colors: {', '.join(context['colors']['text'][:3]) if context['colors']['text'] else '#333333'}
- All Colors Found: {', '.join(context['colors']['all_colors'][:10]) if context['colors']['all_colors'] else 'Default'}

NAVIGATION:
- Menu Items: {json.dumps(context['navigation']['menu_items'][:5], indent=2)}
- Has Dropdown: {context['navigation']['has_dropdown']}
- Is Sticky: {context['navigation']['is_sticky']}

COMPONENTS DETECTED:
{json.dumps(context['components'], indent=2)}

RESPONSIVE DESIGN:
- Has Viewport Meta: {context['responsive']['has_viewport_meta']}
- Uses Responsive Images: {context['responsive']['uses_responsive_images']}
- Has Mobile Menu: {context['responsive']['has_mobile_menu']}

SPECIAL FEATURES:
{', '.join(context['features']) if context['features'] else 'None detected'}

REQUIREMENTS:
1. Create a complete, valid HTML5 document
2. Include all CSS inline in a <style> tag
3. Match the color scheme and typography as closely as possible
4. Implement the same layout structure (header, main, footer, etc.)
5. Include responsive design with media queries
6. Add smooth transitions and hover effects
7. Ensure accessibility with proper semantic HTML
8. Include the navigation menu with similar styling
9. Add placeholder content that matches the theme
10. Make it visually appealing and professional

Generate the complete HTML code:
"""
        return prompt
    
    async def _generate_with_template(self, context: Dict[str, Any]) -> str:
        """Generate HTML using advanced template system"""
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        # Extract key design elements
        bg_color = self._get_primary_color(context['colors']['background'], '#ffffff')
        text_color = self._get_primary_color(context['colors']['text'], '#333333')
        primary_color = self._get_primary_color(context['colors']['all_colors'], '#007bff')
        
        # Get fonts
        fonts = context['typography']['fonts'] if context['typography']['fonts'] else ['-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif']
        primary_font = self._clean_font_family(fonts[0] if fonts else 'sans-serif')
        
        # Determine if dark theme
        is_dark = self._is_dark_theme(bg_color)
        
        # Generate navigation HTML
        nav_html = self._generate_navigation(context['navigation'], primary_color, is_dark)
        
        # Generate main content based on layout type
        main_content = self._generate_main_content(context, primary_color)
        
        # Generate component sections
        components_html = self._generate_components(context['components'], primary_color)
        
        # Build the complete HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{context['title']} - AI Clone</title>
    <meta name="description" content="{context['meta'].get('description', 'AI-generated clone of ' + context['url'])}">
    <meta name="theme-color" content="{context['meta'].get('theme-color', primary_color)}">
    
    <style>
        /* Reset and Base Styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: {primary_color};
            --bg-color: {bg_color};
            --text-color: {text_color};
            --secondary-bg: {self._adjust_brightness(bg_color, 0.05 if is_dark else -0.05)};
            --border-color: {text_color}22;
            --shadow-color: {self._get_shadow_color(is_dark)};
        }}
        
        body {{
            font-family: {primary_font};
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            margin-bottom: 1rem;
            line-height: 1.2;
            font-weight: 600;
        }}
        
        h1 {{ font-size: 2.5rem; }}
        h2 {{ font-size: 2rem; }}
        h3 {{ font-size: 1.75rem; }}
        h4 {{ font-size: 1.5rem; }}
        h5 {{ font-size: 1.25rem; }}
        h6 {{ font-size: 1rem; }}
        
        p {{
            margin-bottom: 1rem;
        }}
        
        a {{
            color: var(--primary-color);
            text-decoration: none;
            transition: opacity 0.3s ease;
        }}
        
        a:hover {{
            opacity: 0.8;
        }}
        
        /* Container */
        .container {{
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Navigation Styles */
        nav {{
            background-color: var(--secondary-bg);
            border-bottom: 1px solid var(--border-color);
            {f'position: sticky; top: 0; z-index: 1000;' if context['navigation']['is_sticky'] else ''}
        }}
        
        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }}
        
        .nav-logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--text-color);
        }}
        
        .nav-menu {{
            display: flex;
            list-style: none;
            gap: 2rem;
            align-items: center;
        }}
        
        .nav-menu a {{
            color: var(--text-color);
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            transition: background-color 0.3s ease;
        }}
        
        .nav-menu a:hover {{
            background-color: var(--primary-color)22;
        }}
        
        .mobile-menu-toggle {{
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-color);
        }}
        
        /* Main Content */
        main {{
            flex: 1;
            padding: 3rem 0;
        }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, var(--primary-color)22 0%, var(--primary-color)11 100%);
            padding: 4rem 2rem;
            border-radius: 1rem;
            margin-bottom: 3rem;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, var(--primary-color), {self._adjust_brightness(primary_color, 0.2)});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .hero p {{
            font-size: 1.25rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }}
        
        /* Button Styles */
        .button {{
            display: inline-block;
            background-color: var(--primary-color);
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 0.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px var(--shadow-color);
        }}
        
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px var(--shadow-color);
            opacity: 1;
        }}
        
        .button-secondary {{
            background-color: transparent;
            color: var(--primary-color);
            border: 2px solid var(--primary-color);
        }}
        
        .button-secondary:hover {{
            background-color: var(--primary-color);
            color: white;
        }}
        
        /* Grid Layout */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }}
        
        /* Card Component */
        .card {{
            background-color: var(--secondary-bg);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            padding: 2rem;
            transition: all 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px var(--shadow-color);
        }}
        
        .card h3 {{
            color: var(--primary-color);
            margin-bottom: 1rem;
        }}
        
        .card p {{
            opacity: 0.8;
        }}
        
        /* Feature Section */
        .features {{
            padding: 4rem 0;
            background-color: var(--secondary-bg);
            border-radius: 1rem;
            margin: 3rem 0;
        }}
        
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 3rem;
            margin-top: 3rem;
        }}
        
        .feature {{
            text-align: center;
        }}
        
        .feature-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }}
        
        /* Footer */
        footer {{
            background-color: var(--secondary-bg);
            border-top: 1px solid var(--border-color);
            padding: 3rem 0 2rem;
            margin-top: 4rem;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .footer-section h4 {{
            margin-bottom: 1rem;
            color: var(--primary-color);
        }}
        
        .footer-section ul {{
            list-style: none;
        }}
        
        .footer-section ul li {{
            margin-bottom: 0.5rem;
        }}
        
        .footer-bottom {{
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
            opacity: 0.7;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .nav-menu {{
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background-color: var(--secondary-bg);
                flex-direction: column;
                padding: 1rem;
                box-shadow: 0 4px 6px var(--shadow-color);
            }}
            
            .nav-menu.active {{
                display: flex;
            }}
            
            .mobile-menu-toggle {{
                display: block;
            }}
            
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .grid {{
                grid-template-columns: 1fr;
            }}
            
            .footer-content {{
                grid-template-columns: 1fr;
                text-align: center;
            }}
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s ease-out;
        }}
        
        /* Utility Classes */
        .text-center {{ text-align: center; }}
        .mt-1 {{ margin-top: 0.5rem; }}
        .mt-2 {{ margin-top: 1rem; }}
        .mt-3 {{ margin-top: 1.5rem; }}
        .mt-4 {{ margin-top: 2rem; }}
        .mb-1 {{ margin-bottom: 0.5rem; }}
        .mb-2 {{ margin-bottom: 1rem; }}
        .mb-3 {{ margin-bottom: 1.5rem; }}
        .mb-4 {{ margin-bottom: 2rem; }}
    </style>
</head>
<body>
    {nav_html}
    
    <main class="fade-in">
        <div class="container">
            {main_content}
            {components_html}
        </div>
    </main>
    
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>About This Clone</h4>
                    <p>This is an AI-generated clone of {context['url']}, created using advanced web scraping and LLM technology.</p>
                </div>
                <div class="footer-section">
                    <h4>Features</h4>
                    <ul>
                        <li>✨ AI-Powered Design</li>
                        <li>📱 Responsive Layout</li>
                        <li>🎨 Matched Color Scheme</li>
                        <li>⚡ Fast Performance</li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Technology</h4>
                    <ul>
                        <li>Built with Orchids Cloner</li>
                        <li>Powered by Claude AI</li>
                        <li>HTML5 & CSS3</li>
                        <li>Mobile-First Design</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                <p>Original site: <a href="{context['url']}" target="_blank">{context['domain']}</a></p>
            </div>
        </div>
    </footer>
    
    <script>
        // Mobile menu toggle
        document.addEventListener('DOMContentLoaded', function() {{
            const menuToggle = document.querySelector('.mobile-menu-toggle');
            const navMenu = document.querySelector('.nav-menu');
            
            if (menuToggle) {{
                menuToggle.addEventListener('click', function() {{
                    navMenu.classList.toggle('active');
                    this.textContent = navMenu.classList.contains('active') ? '✕' : '☰';
                }});
            }}
            
            // Smooth scroll for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {{
                        target.scrollIntoView({{
                            behavior: 'smooth',
                            block: 'start'
                        }});
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_navigation(self, nav_data: Dict[str, Any], primary_color: str, is_dark: bool) -> str:
        """Generate navigation HTML"""
        menu_items = nav_data['menu_items'][:5] if nav_data['menu_items'] else [
            {"text": "Home", "href": "#"},
            {"text": "About", "href": "#about"},
            {"text": "Services", "href": "#services"},
            {"text": "Contact", "href": "#contact"}
        ]
        
        menu_html = '\n'.join([
            f'<li><a href="{item["href"]}">{item["text"]}</a></li>'
            for item in menu_items
        ])
        
        return f"""
    <nav>
        <div class="container">
            <div class="nav-container">
                <div class="nav-logo">
                    <a href="#">Clone Site</a>
                </div>
                <ul class="nav-menu">
                    {menu_html}
                </ul>
                <button class="mobile-menu-toggle">☰</button>
            </div>
        </div>
    </nav>"""
    
    def _generate_main_content(self, context: Dict[str, Any], primary_color: str) -> str:
        """Generate main content based on layout type"""
        layout_type = context['layout']['layout_type']
        
        hero_section = f"""
            <section class="hero">
                <h1>{context['title']}</h1>
                <p>{context['meta'].get('description', 'Welcome to our AI-cloned website. Experience the power of intelligent web design recreation.')}</p>
                <div style="margin-top: 2rem;">
                    <a href="{context['url']}" class="button" target="_blank">View Original</a>
                    <a href="#features" class="button button-secondary" style="margin-left: 1rem;">Learn More</a>
                </div>
            </section>
        """
        
        if layout_type == "sidebar":
            return hero_section + self._generate_sidebar_layout(context)
        elif layout_type == "multi-section":
            return hero_section + self._generate_multi_section_layout(context)
        else:
            return hero_section + self._generate_single_column_layout(context)
    
    def _generate_sidebar_layout(self, context: Dict[str, Any]) -> str:
        """Generate sidebar layout"""
        return """
            <div style="display: grid; grid-template-columns: 1fr 300px; gap: 2rem; margin-top: 3rem;">
                <div>
                    <h2>Main Content</h2>
                    <p>This layout includes a sidebar, mimicking the original website's structure. The content flows naturally with the sidebar providing additional information and navigation options.</p>
                    
                    <div class="grid" style="grid-template-columns: repeat(2, 1fr);">
                        <div class="card">
                            <h3>Feature One</h3>
                            <p>Advanced AI technology ensures accurate design replication.</p>
                        </div>
                        <div class="card">
                            <h3>Feature Two</h3>
                            <p>Responsive design that works on all devices and screen sizes.</p>
                        </div>
                    </div>
                </div>
                
                <aside style="background: var(--secondary-bg); padding: 2rem; border-radius: 0.75rem;">
                    <h3>Sidebar</h3>
                    <p>Additional content and links that complement the main content area.</p>
                    <ul style="list-style: none; margin-top: 1rem;">
                        <li style="margin-bottom: 0.5rem;"><a href="#">Related Link 1</a></li>
                        <li style="margin-bottom: 0.5rem;"><a href="#">Related Link 2</a></li>
                        <li style="margin-bottom: 0.5rem;"><a href="#">Related Link 3</a></li>
                    </ul>
                </aside>
            </div>
        """
    
    def _generate_multi_section_layout(self, context: Dict[str, Any]) -> str:
        """Generate multi-section layout"""
        sections_count = min(context['structure']['main_sections'], 4)
        sections_html = ""
        
        section_contents = [
            ("About Us", "Learn about our advanced AI-powered website cloning technology and how it can help you recreate any website design with precision."),
            ("Our Process", "We use cutting-edge web scraping combined with large language models to analyze and recreate website aesthetics accurately."),
            ("Benefits", "Save time and resources by instantly generating HTML clones of websites for inspiration, analysis, or development purposes."),
            ("Get Started", "Experience the power of AI-driven web design replication. Try our service today and see the results for yourself.")
        ]
        
        for i in range(sections_count):
            title, content = section_contents[i] if i < len(section_contents) else (f"Section {i+1}", "Content for this section.")
            sections_html += f"""
            <section style="margin: 3rem 0; padding: 2rem 0; border-bottom: 1px solid var(--border-color);">
                <h2>{title}</h2>
                <p>{content}</p>
            </section>
            """
        
        return sections_html
    
    def _generate_single_column_layout(self, context: Dict[str, Any]) -> str:
        """Generate single column layout"""
        return """
            <article style="max-width: 800px; margin: 3rem auto;">
                <h2>Welcome to Your Cloned Website</h2>
                <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;">
                    This AI-generated clone captures the essence of the original website's design, layout, and aesthetic choices. 
                    Our advanced technology analyzes color schemes, typography, component structures, and responsive behaviors 
                    to create an accurate representation.
                </p>
                
                <h3>Key Features Replicated</h3>
                <ul style="line-height: 2; margin-bottom: 2rem;">
                    <li>Original color palette and theme</li>
                    <li>Typography and font choices</li>
                    <li>Layout structure and spacing</li>
                    <li>Responsive design patterns</li>
                    <li>Component styles and interactions</li>
                </ul>
                
                <div class="card" style="margin: 2rem 0;">
                    <h3>Technology Stack</h3>
                    <p>Built using modern web technologies and AI-powered design analysis to ensure the highest quality replication.</p>
                </div>
            </article>
        """
    
    def _generate_components(self, components: Dict[str, bool], primary_color: str) -> str:
        """Generate HTML for detected components"""
        components_html = ""
        
        if components.get('cards'):
            components_html += """
            <section id="features" class="features">
                <h2 class="text-center">Features & Capabilities</h2>
                <div class="feature-grid">
                    <div class="feature">
                        <span class="feature-icon">🎨</span>
                        <h3>Design Analysis</h3>
                        <p>Advanced AI analyzes design patterns, colors, and layouts.</p>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">⚡</span>
                        <h3>Fast Generation</h3>
                        <p>Get your cloned website in seconds, not hours.</p>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">📱</span>
                        <h3>Mobile Ready</h3>
                        <p>All clones are responsive and mobile-optimized.</p>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🔧</span>
                        <h3>Clean Code</h3>
                        <p>Generated HTML is clean, semantic, and well-structured.</p>
                    </div>
                </div>
            </section>
            """
        
        if components.get('forms'):
            components_html += f"""
            <section style="margin: 3rem 0; padding: 3rem; background: var(--secondary-bg); border-radius: 1rem;">
                <h2 class="text-center">Get In Touch</h2>
                <form style="max-width: 600px; margin: 2rem auto;">
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem;">Name</label>
                        <input type="text" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 0.25rem; background: var(--bg-color); color: var(--text-color);">
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem;">Email</label>
                        <input type="email" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 0.25rem; background: var(--bg-color); color: var(--text-color);">
                    </div>
                    <div style="margin-bottom: 1.5rem;">
                        <label style="display: block; margin-bottom: 0.5rem;">Message</label>
                        <textarea rows="4" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 0.25rem; background: var(--bg-color); color: var(--text-color);"></textarea>
                    </div>
                    <button type="submit" class="button" style="width: 100%;">Send Message</button>
                </form>
            </section>
            """
        
        return components_html
    
    def _get_primary_color(self, colors: list, default: str) -> str:
        """Extract primary color from list"""
        if not colors:
            return default
        
        # Clean and return first valid color
        for color in colors:
            color = color.strip()
            if color.startswith('#') or color.startswith('rgb'):
                return color
        
        return default
    
    def _clean_font_family(self, font: str) -> str:
        """Clean font family string"""
        font = font.strip().strip('"\'')
        if not font or font == 'inherit':
            return '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        return font
    
    def _is_dark_theme(self, bg_color: str) -> bool:
        """Determine if background color is dark"""
        if not bg_color.startswith('#'):
            return False
        
        try:
            # Convert hex to RGB
            hex_color = bg_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Calculate luminance
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return luminance < 0.5
        except:
            return False
    
    def _adjust_brightness(self, color: str, factor: float) -> str:
        """Adjust color brightness"""
        if not color.startswith('#'):
            return color
        
        try:
            hex_color = color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Adjust brightness
            r = max(0, min(255, int(r * (1 + factor))))
            g = max(0, min(255, int(g * (1 + factor))))
            b = max(0, min(255, int(b * (1 + factor))))
            
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return color
    
    def _get_shadow_color(self, is_dark: bool) -> str:
        """Get appropriate shadow color based on theme"""
        return 'rgba(255, 255, 255, 0.1)' if is_dark else 'rgba(0, 0, 0, 0.1)'

# Utility function for easy integration
async def generate_html_clone(design_context: Dict[str, Any]) -> str:
    """Generate HTML clone using LLM"""
    generator = LLMGenerator()
    return await generator.generate_html(design_context)