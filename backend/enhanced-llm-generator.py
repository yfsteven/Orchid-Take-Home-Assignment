import os
import json
from typing import Dict, Any, Optional, List
import asyncio
from datetime import datetime
import anthropic
from anthropic import AsyncAnthropic

class EnhancedLLMGenerator:
    """Enhanced LLM integration with Claude API for generating HTML clones"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY', '')
        self.use_claude_api = bool(self.api_key)
        
        if self.use_claude_api:
            self.client = AsyncAnthropic(api_key=self.api_key)
            self.model = "claude-3-5-sonnet-20241022"  # Latest Claude model
        else:
            print("No Anthropic API key found. Using template-based generation.")
    
    async def generate_html(self, design_context: Dict[str, Any]) -> str:
        """Generate HTML based on scraped design context"""
        
        if self.use_claude_api:
            try:
                # Use Claude API for generation
                return await self._generate_with_claude(design_context)
            except Exception as e:
                print(f"Claude API error: {e}. Falling back to template generation.")
                return await self._generate_with_advanced_template(design_context)
        else:
            # Use advanced template generation
            return await self._generate_with_advanced_template(design_context)
    
    async def _generate_with_claude(self, context: Dict[str, Any]) -> str:
        """Generate HTML using Claude API with advanced prompting"""
        
        # Create a comprehensive prompt with chain-of-thought reasoning
        system_prompt = """You are an expert web developer and designer specializing in creating pixel-perfect HTML clones of websites. Your task is to generate a complete, single-file HTML document that closely matches the original website's aesthetics based on the provided design context.

Your approach should be:
1. Analyze the design context thoroughly
2. Identify the key visual elements and patterns
3. Create semantic HTML structure
4. Write comprehensive CSS that matches the original design
5. Add interactive JavaScript for enhanced user experience
6. Ensure full responsiveness across all devices
7. Optimize for performance and accessibility

Always output a complete, valid HTML5 document with all CSS and JavaScript inline."""

        # Create structured prompt with design context
        user_prompt = self._create_structured_prompt(context)
        
        # Add screenshots if available
        messages = [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        # If we have screenshots, add them as base64 images
        if 'screenshots' in context and context['screenshots']:
            screenshot_content = []
            if 'viewport' in context['screenshots']:
                screenshot_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": context['screenshots']['viewport']
                    }
                })
            
            if screenshot_content:
                messages[0]["content"] = [
                    {"type": "text", "text": user_prompt},
                    *screenshot_content
                ]
        
        # Call Claude API
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            temperature=0.3,  # Lower temperature for more consistent output
            system=system_prompt,
            messages=messages
        )
        
        # Extract HTML from response
        html_content = response.content[0].text
        
        # Post-process to ensure valid HTML
        return self._post_process_html(html_content)
    
    def _create_structured_prompt(self, context: Dict[str, Any]) -> str:
        """Create a detailed, structured prompt for Claude"""
        
        # Build component list
        detected_components = []
        for comp, exists in context.get('components', {}).items():
            if exists:
                detected_components.append(comp)
        
        # Build feature list
        features = context.get('features', [])
        
        # Create color palette description
        colors = context.get('colors', {})
        color_description = f"""
Primary Colors:
- Background: {', '.join(colors.get('background', ['#ffffff'])[:3])}
- Text: {', '.join(colors.get('text', ['#333333'])[:3])}
- All detected colors: {', '.join(colors.get('all_colors', [])[:15])}
"""
        
        # Navigation structure
        nav_items = context.get('navigation', {}).get('menu_items', [])
        nav_structure = "\n".join([f"  - {item['text']} ({item['href']})" for item in nav_items[:10]])
        
        prompt = f"""Create an HTML clone of the website: {context['url']}

CRITICAL REQUIREMENTS:
1. Match the visual design as closely as possible
2. Use the exact color palette detected
3. Implement the same layout structure
4. Include all detected components
5. Ensure full responsiveness
6. Add smooth animations and transitions

DESIGN CONTEXT:

**Basic Information:**
- Title: {context['title']}
- Domain: {context['domain']}
- Meta Description: {context.get('meta', {}).get('description', 'N/A')}

**Color Palette:**
{color_description}

**Typography:**
- Primary Fonts: {', '.join(context['typography']['fonts'][:3]) if context['typography']['fonts'] else 'System default'}
- Font Sizes: {', '.join(context['typography']['font_sizes'][:8]) if context['typography']['font_sizes'] else 'Default'}

**Layout Structure:**
- Type: {context['layout']['layout_type']}
- Has Header: {context['structure']['has_header']}
- Has Footer: {context['structure']['has_footer']}
- Has Sidebar: {context['structure']['has_sidebar']}
- Main Sections: {context['structure']['main_sections']}
- Header Height: {context['structure'].get('header_height', 'Auto')}px
- Footer Height: {context['structure'].get('footer_height', 'Auto')}px

**Navigation:**
- Sticky Navigation: {context['navigation']['is_sticky']}
- Has Dropdown: {context['navigation']['has_dropdown']}
- Menu Items:
{nav_structure}

**Components Detected:**
{', '.join(detected_components) if detected_components else 'Basic components only'}

**Special Features:**
{', '.join(features) if features else 'Standard features'}

**Responsive Design:**
- Viewport Meta: {context['responsive']['has_viewport_meta']}
- Responsive Images: {context['responsive']['uses_responsive_images']}
- Mobile Menu: {context['responsive']['has_mobile_menu']}

**Typography Details:**
{json.dumps(context['typography'].get('headings', {}), indent=2)}

Generate a complete HTML document that:
1. Uses semantic HTML5 elements
2. Includes all CSS in a <style> tag
3. Implements the exact color scheme
4. Matches the typography hierarchy
5. Recreates the layout structure
6. Includes smooth hover effects and transitions
7. Is fully responsive with appropriate breakpoints
8. Includes interactive JavaScript for navigation and UI elements
9. Has proper meta tags for SEO
10. Follows accessibility best practices

The HTML should be production-ready and visually identical to the original site."""
        
        return prompt
    
    async def _generate_with_advanced_template(self, context: Dict[str, Any]) -> str:
        """Enhanced template-based generation with more sophisticated patterns"""
        
        # Simulate processing
        await asyncio.sleep(0.5)
        
        # Extract design elements with better defaults
        colors = self._extract_color_scheme(context['colors'])
        typography = self._extract_typography(context['typography'])
        layout = self._determine_layout_strategy(context)
        
        # Generate sections based on detected components
        sections = []
        
        # Hero section
        sections.append(self._generate_hero_section(context, colors))
        
        # Feature section if cards detected
        if context['components'].get('cards'):
            sections.append(self._generate_feature_cards(colors))
        
        # Gallery section if images detected
        if context['components'].get('buttons', 0) > 5:
            sections.append(self._generate_gallery_section(colors))
        
        # Contact section if forms detected
        if context['components'].get('forms'):
            sections.append(self._generate_contact_section(colors))
        
        # Generate the complete HTML
        html = self._build_complete_html(
            context=context,
            colors=colors,
            typography=typography,
            layout=layout,
            sections=sections
        )
        
        return html
    
    def _extract_color_scheme(self, color_data: Dict[str, List[str]]) -> Dict[str, str]:
        """Extract a cohesive color scheme from the scraped colors"""
        
        # Get primary colors
        bg_colors = color_data.get('background', ['#ffffff'])
        text_colors = color_data.get('text', ['#333333'])
        all_colors = color_data.get('all_colors', [])
        
        # Find primary accent color (not white/black/gray)
        accent_color = '#007bff'  # Default
        for color in all_colors:
            if not self._is_grayscale(color):
                accent_color = color
                break
        
        # Determine theme
        primary_bg = self._get_primary_color(bg_colors, '#ffffff')
        is_dark = self._is_dark_theme(primary_bg)
        
        return {
            'background': primary_bg,
            'text': self._get_primary_color(text_colors, '#333333' if not is_dark else '#ffffff'),
            'accent': accent_color,
            'secondary_bg': self._adjust_brightness(primary_bg, 0.05 if is_dark else -0.05),
            'border': f"{text_colors[0]}22" if text_colors else '#00000022',
            'shadow': 'rgba(255,255,255,0.1)' if is_dark else 'rgba(0,0,0,0.1)',
            'is_dark': is_dark
        }
    
    def _extract_typography(self, typography_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract typography system"""
        fonts = typography_data.get('fonts', [])
        primary_font = self._clean_font_family(fonts[0] if fonts else 'system-ui')
        
        # Get heading styles
        headings = typography_data.get('headings', {})
        
        return {
            'primary_font': primary_font,
            'secondary_font': self._clean_font_family(fonts[1] if len(fonts) > 1 else primary_font),
            'sizes': typography_data.get('font_sizes', ['16px']),
            'headings': headings
        }
    
    def _determine_layout_strategy(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Determine the best layout strategy based on the original site"""
        layout_type = context['layout']['layout_type']
        
        strategies = {
            'sidebar': {
                'container': 'container-fluid',
                'main_layout': 'grid',
                'grid_template': '"header header" auto "sidebar main" 1fr "footer footer" auto / 280px 1fr'
            },
            'multi-section': {
                'container': 'container',
                'main_layout': 'sections',
                'section_spacing': '5rem'
            },
            'single-column': {
                'container': 'container',
                'main_layout': 'article',
                'max_width': '800px'
            }
        }
        
        return strategies.get(layout_type, strategies['single-column'])
    
    def _generate_hero_section(self, context: Dict[str, Any], colors: Dict[str, str]) -> str:
        """Generate an impressive hero section"""
        return f"""
    <section class="hero-section">
        <div class="hero-background"></div>
        <div class="hero-content">
            <h1 class="hero-title animate-fade-up">{context['title']}</h1>
            <p class="hero-subtitle animate-fade-up-delay">
                {context.get('meta', {}).get('description', 'Experience the perfect blend of design and functionality')}
            </p>
            <div class="hero-actions animate-fade-up-delay-2">
                <a href="{context['url']}" class="btn btn-primary btn-lg" target="_blank">
                    View Original
                </a>
                <a href="#features" class="btn btn-outline btn-lg">
                    Explore Clone
                </a>
            </div>
        </div>
        <div class="hero-scroll-indicator">
            <span>Scroll</span>
            <div class="scroll-arrow"></div>
        </div>
    </section>"""
    
    def _generate_feature_cards(self, colors: Dict[str, str]) -> str:
        """Generate feature cards section"""
        features = [
            ("🎨", "Pixel-Perfect Design", "Every detail meticulously recreated to match the original aesthetic"),
            ("⚡", "Lightning Fast", "Optimized performance with minimal load times"),
            ("📱", "Fully Responsive", "Seamless experience across all devices and screen sizes"),
            ("🔧", "Clean Code", "Well-structured, semantic HTML with modern CSS")
        ]
        
        cards = '\n'.join([
            f"""
            <div class="feature-card animate-on-scroll">
                <div class="feature-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>"""
            for icon, title, desc in features
        ])
        
        return f"""
    <section id="features" class="features-section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Key Features</h2>
                <p class="section-subtitle">Built with cutting-edge technology</p>
            </div>
            <div class="features-grid">
                {cards}
            </div>
        </div>
    </section>"""
    
    def _generate_gallery_section(self, colors: Dict[str, str]) -> str:
        """Generate a gallery/portfolio section"""
        return """
    <section class="gallery-section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Visual Excellence</h2>
                <p class="section-subtitle">Showcasing design precision</p>
            </div>
            <div class="gallery-grid">
                <div class="gallery-item animate-on-scroll">
                    <div class="gallery-image">
                        <div class="placeholder-image gradient-1"></div>
                    </div>
                    <div class="gallery-overlay">
                        <h4>Modern Design</h4>
                    </div>
                </div>
                <div class="gallery-item animate-on-scroll">
                    <div class="gallery-image">
                        <div class="placeholder-image gradient-2"></div>
                    </div>
                    <div class="gallery-overlay">
                        <h4>Responsive Layout</h4>
                    </div>
                </div>
                <div class="gallery-item animate-on-scroll">
                    <div class="gallery-image">
                        <div class="placeholder-image gradient-3"></div>
                    </div>
                    <div class="gallery-overlay">
                        <h4>Clean Interface</h4>
                    </div>
                </div>
            </div>
        </div>
    </section>"""
    
    def _generate_contact_section(self, colors: Dict[str, str]) -> str:
        """Generate contact form section"""
        return """
    <section class="contact-section" id="contact">
        <div class="container">
            <div class="contact-wrapper">
                <div class="contact-info">
                    <h2>Get In Touch</h2>
                    <p>Experience the power of AI-driven web cloning</p>
                    <div class="contact-details">
                        <div class="contact-item">
                            <span class="contact-icon">📧</span>
                            <span>contact@example.com</span>
                        </div>
                        <div class="contact-item">
                            <span class="contact-icon">🌐</span>
                            <span>www.example.com</span>
                        </div>
                    </div>
                </div>
                <form class="contact-form">
                    <div class="form-group">
                        <input type="text" placeholder="Your Name" required>
                    </div>
                    <div class="form-group">
                        <input type="email" placeholder="Your Email" required>
                    </div>
                    <div class="form-group">
                        <textarea placeholder="Your Message" rows="5" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">
                        Send Message
                    </button>
                </form>
            </div>
        </div>
    </section>"""
    
    def _build_complete_html(self, context: Dict[str, Any], colors: Dict[str, str], 
                            typography: Dict[str, Any], layout: Dict[str, str], 
                            sections: List[str]) -> str:
        """Build the complete HTML document"""
        
        # Generate navigation
        nav_html = self._generate_navigation(context['navigation'], colors)
        
        # Generate CSS with all styles
        css = self._generate_comprehensive_css(colors, typography, layout)
        
        # Generate JavaScript
        js = self._generate_javascript()
        
        # Join sections
        sections_html = '\n'.join(sections)
        
        # Build complete HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{context['title']} - AI Clone</title>
    <meta name="description" content="{context.get('meta', {}).get('description', 'AI-generated clone')}">
    <meta name="theme-color" content="{colors['accent']}">
    
    <!-- Preconnect to external resources -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <style>
{css}
    </style>
</head>
<body>
    <!-- Loading Screen -->
    <div class="loading-screen">
        <div class="loader"></div>
    </div>
    
    {nav_html}
    
    <main>
        {sections_html}
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>About This Clone</h4>
                    <p>AI-powered recreation of {context['domain']}</p>
                    <p class="footer-meta">Generated on {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                <div class="footer-section">
                    <h4>Technologies</h4>
                    <ul class="footer-list">
                        <li>Claude AI Integration</li>
                        <li>Advanced Web Scraping</li>
                        <li>Responsive Design</li>
                        <li>Modern CSS & JavaScript</li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Original Site</h4>
                    <p>View the original at:</p>
                    <a href="{context['url']}" target="_blank" class="footer-link">
                        {context['domain']}
                    </a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 AI Website Cloner. Powered by Orchids Technology.</p>
            </div>
        </div>
    </footer>
    
    <script>
{js}
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_comprehensive_css(self, colors: Dict[str, str], typography: Dict[str, Any], 
                                   layout: Dict[str, str]) -> str:
        """Generate comprehensive CSS styles"""
        
        # Create CSS variables for dynamic theming
        css = f"""
        /* CSS Variables */
        :root {{
            --color-bg: {colors['background']};
            --color-text: {colors['text']};
            --color-accent: {colors['accent']};
            --color-secondary-bg: {colors['secondary_bg']};
            --color-border: {colors['border']};
            --color-shadow: {colors['shadow']};
            --font-primary: {typography['primary_font']};
            --font-secondary: {typography['secondary_font']};
            --container-width: 1200px;
            --spacing-unit: 1rem;
            --transition-speed: 0.3s;
            --transition-timing: cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* Reset & Base Styles */
        *, *::before, *::after {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        html {{
            font-size: 16px;
            scroll-behavior: smooth;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        body {{
            font-family: var(--font-primary);
            background-color: var(--color-bg);
            color: var(--color-text);
            line-height: 1.6;
            overflow-x: hidden;
            position: relative;
        }}
        
        /* Loading Screen */
        .loading-screen {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--color-bg);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            transition: opacity 0.5s, visibility 0.5s;
        }}
        
        .loading-screen.loaded {{
            opacity: 0;
            visibility: hidden;
        }}
        
        .loader {{
            width: 50px;
            height: 50px;
            border: 3px solid var(--color-border);
            border-top-color: var(--color-accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-secondary);
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 1em;
        }}
        
        h1 {{ font-size: clamp(2rem, 5vw, 3.5rem); }}
        h2 {{ font-size: clamp(1.75rem, 4vw, 2.5rem); }}
        h3 {{ font-size: clamp(1.5rem, 3vw, 2rem); }}
        h4 {{ font-size: clamp(1.25rem, 2.5vw, 1.75rem); }}
        h5 {{ font-size: clamp(1.125rem, 2vw, 1.5rem); }}
        h6 {{ font-size: clamp(1rem, 1.5vw, 1.25rem); }}
        
        p {{
            margin-bottom: 1em;
        }}
        
        a {{
            color: var(--color-accent);
            text-decoration: none;
            transition: opacity var(--transition-speed) var(--transition-timing);
        }}
        
        a:hover {{
            opacity: 0.8;
        }}
        
        /* Container */
        .container {{
            width: 100%;
            max-width: var(--container-width);
            margin: 0 auto;
            padding: 0 var(--spacing-unit);
        }}
        
        /* Navigation */
        .site-nav {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: var(--color-bg);
            border-bottom: 1px solid var(--color-border);
            z-index: 1000;
            transition: all var(--transition-speed) var(--transition-timing);
        }}
        
        .site-nav.scrolled {{
            background: var(--color-secondary-bg);
            box-shadow: 0 2px 20px var(--color-shadow);
        }}
        
        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }}
        
        .nav-logo {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--color-text);
        }}
        
        .nav-menu {{
            display: flex;
            list-style: none;
            gap: 2rem;
            align-items: center;
        }}
        
        .nav-menu a {{
            color: var(--color-text);
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            transition: all var(--transition-speed) var(--transition-timing);
            position: relative;
        }}
        
        .nav-menu a::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 0;
            height: 2px;
            background: var(--color-accent);
            transform: translateX(-50%);
            transition: width var(--transition-speed) var(--transition-timing);
        }}
        
        .nav-menu a:hover::after {{
            width: 80%;
        }}
        
        .mobile-menu-toggle {{
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--color-text);
        }}
        
        /* Hero Section */
        .hero-section {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            margin-top: -60px;
            padding-top: 60px;
        }}
        
        .hero-background {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, var(--color-accent) 0%, {self._adjust_brightness(colors['accent'], -0.2)} 100%);
            opacity: 0.1;
            z-index: -1;
        }}
        
        .hero-content {{
            text-align: center;
            padding: 2rem;
            max-width: 800px;
        }}
        
        .hero-title {{
            font-size: clamp(2.5rem, 8vw, 5rem);
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, var(--color-accent), {self._adjust_brightness(colors['accent'], 0.3)});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .hero-subtitle {{
            font-size: clamp(1.125rem, 3vw, 1.5rem);
            opacity: 0.9;
            margin-bottom: 2.5rem;
        }}
        
        .hero-actions {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .hero-scroll-indicator {{
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            animation: bounce 2s infinite;
        }}
        
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateX(-50%) translateY(0); }}
            40% {{ transform: translateX(-50%) translateY(-10px); }}
            60% {{ transform: translateX(-50%) translateY(-5px); }}
        }}
        
        /* Buttons */
        .btn {{
            display: inline-block;
            padding: 0.75rem 2rem;
            border-radius: 0.5rem;
            font-weight: 600;
            text-align: center;
            transition: all var(--transition-speed) var(--transition-timing);
            cursor: pointer;
            border: 2px solid transparent;
        }}
        
        .btn-primary {{
            background: var(--color-accent);
            color: white;
            box-shadow: 0 4px 15px var(--color-shadow);
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 25px var(--color-shadow);
            opacity: 1;
        }}
        
        .btn-outline {{
            background: transparent;
            color: var(--color-accent);
            border-color: var(--color-accent);
        }}
        
        .btn-outline:hover {{
            background: var(--color-accent);
            color: white;
            opacity: 1;
        }}
        
        .btn-lg {{
            padding: 1rem 2.5rem;
            font-size: 1.125rem;
        }}
        
        /* Sections */
        section {{
            padding: 5rem 0;
        }}
        
        .section-header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        
        .section-title {{
            margin-bottom: 1rem;
        }}
        
        .section-subtitle {{
            font-size: 1.125rem;
            opacity: 0.8;
        }}
        
        /* Features Section */
        .features-section {{
            background: var(--color-secondary-bg);
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
        }}
        
        .feature-card {{
            background: var(--color-bg);
            padding: 2.5rem;
            border-radius: 1rem;
            text-align: center;
            transition: all var(--transition-speed) var(--transition-timing);
            border: 1px solid var(--color-border);
        }}
        
        .feature-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 40px var(--color-shadow);
        }}
        
        .feature-icon {{
            font-size: 3rem;
            margin-bottom: 1.5rem;
            display: block;
        }}
        
        /* Gallery Section */
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }}
        
        .gallery-item {{
            position: relative;
            overflow: hidden;
            border-radius: 1rem;
            cursor: pointer;
            height: 300px;
        }}
        
        .gallery-image {{
            width: 100%;
            height: 100%;
            position: relative;
        }}
        
        .placeholder-image {{
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
        }}
        
        .gradient-1 {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .gradient-2 {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        .gradient-3 {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}
        
        .gallery-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity var(--transition-speed) var(--transition-timing);
        }}
        
        .gallery-item:hover .gallery-overlay {{
            opacity: 1;
        }}
        
        .gallery-overlay h4 {{
            color: white;
            margin: 0;
        }}
        
        /* Contact Section */
        .contact-section {{
            background: var(--color-secondary-bg);
        }}
        
        .contact-wrapper {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: start;
        }}
        
        .contact-info h2 {{
            margin-bottom: 1rem;
        }}
        
        .contact-details {{
            margin-top: 2rem;
        }}
        
        .contact-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        
        .contact-icon {{
            font-size: 1.5rem;
        }}
        
        .contact-form {{
            background: var(--color-bg);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 10px 30px var(--color-shadow);
        }}
        
        .form-group {{
            margin-bottom: 1.5rem;
        }}
        
        .form-group input,
        .form-group textarea {{
            width: 100%;
            padding: 1rem;
            border: 1px solid var(--color-border);
            border-radius: 0.5rem;
            background: var(--color-bg);
            color: var(--color-text);
            font-family: inherit;
            transition: border-color var(--transition-speed) var(--transition-timing);
        }}
        
        .form-group input:focus,
        .form-group textarea:focus {{
            outline: none;
            border-color: var(--color-accent);
        }}
        
        .btn-block {{
            width: 100%;
        }}
        
        /* Footer */
        .site-footer {{
            background: var(--color-secondary-bg);
            border-top: 1px solid var(--color-border);
            padding: 3rem 0 1rem;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .footer-section h4 {{
            margin-bottom: 1rem;
            color: var(--color-accent);
        }}
        
        .footer-list {{
            list-style: none;
        }}
        
        .footer-list li {{
            margin-bottom: 0.5rem;
            padding-left: 1rem;
            position: relative;
        }}
        
        .footer-list li::before {{
            content: '→';
            position: absolute;
            left: 0;
            color: var(--color-accent);
        }}
        
        .footer-link {{
            color: var(--color-accent);
            font-weight: 500;
        }}
        
        .footer-meta {{
            font-size: 0.875rem;
            opacity: 0.7;
            margin-top: 0.5rem;
        }}
        
        .footer-bottom {{
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid var(--color-border);
            opacity: 0.7;
            font-size: 0.875rem;
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
        
        .animate-fade-up {{
            animation: fadeIn 0.8s ease-out;
        }}
        
        .animate-fade-up-delay {{
            animation: fadeIn 0.8s ease-out 0.2s both;
        }}
        
        .animate-fade-up-delay-2 {{
            animation: fadeIn 0.8s ease-out 0.4s both;
        }}
        
        .animate-on-scroll {{
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s var(--transition-timing);
        }}
        
        .animate-on-scroll.visible {{
            opacity: 1;
            transform: translateY(0);
        }}
        
        /* Responsive Design */
        @media (max-width: 1024px) {{
            .contact-wrapper {{
                grid-template-columns: 1fr;
            }}
        }}
        
        @media (max-width: 768px) {{
            .nav-menu {{
                position: fixed;
                top: 60px;
                left: 0;
                right: 0;
                background: var(--color-secondary-bg);
                flex-direction: column;
                padding: 2rem;
                transform: translateX(-100%);
                transition: transform var(--transition-speed) var(--transition-timing);
                box-shadow: 0 4px 20px var(--color-shadow);
            }}
            
            .nav-menu.active {{
                transform: translateX(0);
            }}
            
            .mobile-menu-toggle {{
                display: block;
            }}
            
            .hero-actions {{
                flex-direction: column;
                align-items: center;
            }}
            
            .btn {{
                width: 100%;
                max-width: 300px;
            }}
            
            .features-grid,
            .gallery-grid {{
                grid-template-columns: 1fr;
            }}
            
            .footer-content {{
                text-align: center;
            }}
            
            .footer-list li {{
                padding-left: 0;
            }}
            
            .footer-list li::before {{
                display: none;
            }}
        }}
        
        /* Print Styles */
        @media print {{
            .site-nav,
            .hero-scroll-indicator,
            .mobile-menu-toggle {{
                display: none;
            }}
            
            body {{
                color: black;
                background: white;
            }}
        }}"""
        
        return css
    
    def _generate_javascript(self) -> str:
        """Generate JavaScript for interactivity"""
        return """
        // DOM Content Loaded
        document.addEventListener('DOMContentLoaded', function() {
            // Remove loading screen
            setTimeout(() => {
                document.querySelector('.loading-screen').classList.add('loaded');
            }, 500);
            
            // Mobile menu toggle
            const menuToggle = document.querySelector('.mobile-menu-toggle');
            const navMenu = document.querySelector('.nav-menu');
            
            if (menuToggle) {
                menuToggle.addEventListener('click', function() {
                    navMenu.classList.toggle('active');
                    this.innerHTML = navMenu.classList.contains('active') ? '✕' : '☰';
                });
            }
            
            // Navbar scroll effect
            const navbar = document.querySelector('.site-nav');
            let lastScroll = 0;
            
            window.addEventListener('scroll', () => {
                const currentScroll = window.pageYOffset;
                
                if (currentScroll > 50) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
                
                lastScroll = currentScroll;
            });
            
            // Smooth scroll for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    
                    if (target) {
                        const offset = 80; // Navbar height
                        const targetPosition = target.offsetTop - offset;
                        
                        window.scrollTo({
                            top: targetPosition,
                            behavior: 'smooth'
                        });
                        
                        // Close mobile menu if open
                        navMenu.classList.remove('active');
                        if (menuToggle) menuToggle.innerHTML = '☰';
                    }
                });
            });
            
            // Scroll animations
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, observerOptions);
            
            document.querySelectorAll('.animate-on-scroll').forEach(el => {
                observer.observe(el);
            });
            
            // Form submission
            const contactForm = document.querySelector('.contact-form');
            if (contactForm) {
                contactForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    // Simulate form submission
                    const button = this.querySelector('button[type="submit"]');
                    const originalText = button.textContent;
                    
                    button.textContent = 'Sending...';
                    button.disabled = true;
                    
                    setTimeout(() => {
                        button.textContent = 'Message Sent!';
                        button.style.background = '#4caf50';
                        
                        setTimeout(() => {
                            button.textContent = originalText;
                            button.disabled = false;
                            button.style.background = '';
                            this.reset();
                        }, 2000);
                    }, 1500);
                });
            }
            
            // Parallax effect for hero section
            const heroSection = document.querySelector('.hero-section');
            const heroBackground = document.querySelector('.hero-background');
            
            if (heroSection && heroBackground) {
                window.addEventListener('scroll', () => {
                    const scrolled = window.pageYOffset;
                    const rate = scrolled * -0.5;
                    
                    heroBackground.style.transform = `translateY(${rate}px)`;
                });
            }
            
            // Add hover effects to gallery items
            document.querySelectorAll('.gallery-item').forEach(item => {
                item.addEventListener('mouseenter', function() {
                    this.style.transform = 'scale(1.05)';
                });
                
                item.addEventListener('mouseleave', function() {
                    this.style.transform = 'scale(1)';
                });
            });
        });
        
        // Debounce function for performance
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }"""
    
    def _generate_navigation(self, nav_data: Dict[str, Any], colors: Dict[str, str]) -> str:
        """Generate navigation HTML"""
        menu_items = nav_data.get('menu_items', [
            {"text": "Home", "href": "#"},
            {"text": "Features", "href": "#features"},
            {"text": "Gallery", "href": "#gallery"},
            {"text": "Contact", "href": "#contact"}
        ])[:6]
        
        menu_html = '\n'.join([
            f'<li><a href="{item.get("href", "#")}">{item.get("text", "Link")}</a></li>'
            for item in menu_items
        ])
        
        return f"""
    <nav class="site-nav">
        <div class="container">
            <div class="nav-container">
                <div class="nav-logo">
                    <a href="#">Clone Site</a>
                </div>
                <ul class="nav-menu">
                    {menu_html}
                </ul>
                <button class="mobile-menu-toggle" aria-label="Toggle menu">
                    ☰
                </button>
            </div>
        </div>
    </nav>"""
    
    # Helper methods from the original implementation
    def _get_primary_color(self, colors: list, default: str) -> str:
        """Extract primary color from list"""
        if not colors:
            return default
        
        for color in colors:
            color = color.strip()
            if color.startswith('#') or color.startswith('rgb'):
                return color
        
        return default
    
    def _clean_font_family(self, font: str) -> str:
        """Clean font family string"""
        font = font.strip().strip('"\'')
        if not font or font == 'inherit':
            return 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        return font
    
    def _is_dark_theme(self, bg_color: str) -> bool:
        """Determine if background color is dark"""
        if not bg_color.startswith('#'):
            return False
        
        try:
            hex_color = bg_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return luminance < 0.5
        except:
            return False
    
    def _is_grayscale(self, color: str) -> bool:
        """Check if color is grayscale"""
        if not color.startswith('#'):
            return True
        
        try:
            hex_color = color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Check if R, G, B are roughly equal (grayscale)
            return abs(r - g) < 10 and abs(g - b) < 10 and abs(r - b) < 10
        except:
            return True
    
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
    
    def _post_process_html(self, html: str) -> str:
        """Post-process HTML to ensure validity"""
        # Remove any markdown code blocks if present
        html = html.replace('```html', '').replace('```', '')
        
        # Ensure HTML starts with DOCTYPE
        if not html.strip().startswith('<!DOCTYPE'):
            html = '<!DOCTYPE html>\n' + html
        
        return html.strip()

# Convenience function for the main app
async def generate_html_clone(design_context: Dict[str, Any]) -> str:
    """Generate HTML clone using enhanced LLM"""
    generator = EnhancedLLMGenerator()
    return await generator.generate_html(design_context)