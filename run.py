"""
Master Orchestrator & CLI Runner for MexConsumerPulse.
Coordinates the autonomous agent swarm (Reddit, Twitter, Facebook),
triggers data cleaning, runs NLP synthesis, generates daily reports, and exports datasets.
"""

import sys
import argparse
from pathlib import Path

# Add root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from agents.reddit_agent import RedditScraperAgent
from agents.twitter_agent import TwitterScraperAgent
from agents.facebook_agent import FacebookBrowserAgent
from agents.whatsapp_agent import WhatsAppVecinosAgent
from agents.mercadolibre_agent import MercadoLibreAgent
from agents.dataset_manager import DatasetManager
from reports.report_generator import DailyReportGenerator

def main():
    parser = argparse.ArgumentParser(description="MexConsumerPulse: Autonomous Mexican Consumer Research Swarm")
    parser.add_argument("--all", action="store_true", help="Run full pipeline: All agents + Daily Report + Data Export")
    parser.add_argument("--reddit", action="store_true", help="Run Reddit Scraper Agent")
    parser.add_argument("--twitter", action="store_true", help="Run Twitter/X Complaint Agent")
    parser.add_argument("--facebook", action="store_true", help="Run Facebook Groups Browser Agent")
    parser.add_argument("--whatsapp", action="store_true", help="Parse WhatsApp 'Chat de Vecinos' community stream")
    parser.add_argument("--mercadolibre", action="store_true", help="Scrape hot new products and existing product problems from Mercado Libre México (mercadolibre.com.mx)")
    parser.add_argument("--ml-hot", action="store_true", help="Scrape and extract Hot New Products and emerging breakout trends on Mercado Libre México")
    parser.add_argument("--ml-problems", action="store_true", help="Scrape and extract Problems with Existing Products (critical complaints, 1-3 star reviews) on Mercado Libre México")
    parser.add_argument("--ml-login", action="store_true", help="Launch interactive headed browser for Mercado Libre México session capture / human verification")
    parser.add_argument("--fb-login", action="store_true", help="Launch interactive headed browser for Facebook login / 2FA session capture")
    parser.add_argument("--report", action="store_true", help="Generate Daily Intelligence Report only")
    parser.add_argument("--export", action="store_true", help="Export SQLite database to CSV and JSON")
    parser.add_argument("--web", action="store_true", help="Launch FastAPI Web Dashboard server on http://localhost:8000")
    
    args = parser.parse_args()

    # Default to --all if no specific arguments provided
    if not any([args.all, args.reddit, args.twitter, args.facebook, args.whatsapp, args.mercadolibre, args.ml_hot, args.ml_problems, args.ml_login, args.fb_login, args.report, args.export, args.web]):
        args.all = True

    print("=" * 70)
    print(" MEXCONSUMERPULSE: AUTONOMOUS CONSUMER RESEARCH AGENT SWARM")
    print(" Target: Major Mexican Cities (CDMX, GDL, MTY) | Locals & Expats")
    print("=" * 70)

    db = DatasetManager()

    # 0. Launch Web Server
    if args.web:
        import uvicorn
        print("\n[Web Server] Launching MexConsumerPulse Dashboard on http://localhost:8000 ...")
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
        return

    # 1. Interactive Facebook Login
    if args.fb_login:
        fb_agent = FacebookBrowserAgent()
        fb_agent.interactive_login()
        return

    # 1b. Interactive Mercado Libre Session Capture
    if args.ml_login:
        ml_agent = MercadoLibreAgent()
        ml_agent.interactive_session()
        return

    # 2. Reddit Agent
    if args.all or args.reddit:
        print("\n[Stage 1/4] Invoking Reddit Scraper Agent...")
        try:
            reddit_agent = RedditScraperAgent()
            reddit_res = reddit_agent.run(max_per_sub=10)
            print(f" -> Completed: {reddit_res}")
        except Exception as e:
            print(f" [Error] Reddit Agent failed: {e}")

    # 3. Twitter / X Agent
    if args.all or args.twitter:
        print("\n[Stage 2/4] Invoking Twitter / X Complaint Monitoring Agent...")
        try:
            twitter_agent = TwitterScraperAgent()
            twitter_res = twitter_agent.run(max_items=15)
            print(f" -> Completed: {twitter_res}")
        except Exception as e:
            print(f" [Error] Twitter Agent failed: {e}")

    # 4. Facebook Groups Agent
    if args.all or args.facebook:
        print("\n[Stage 3/5] Invoking Facebook Groups Browser Agent...")
        try:
            fb_agent = FacebookBrowserAgent()
            fb_res = fb_agent.run(max_scrolls=3)
            print(f" -> Completed: {fb_res}")
        except Exception as e:
            print(f" [Error] Facebook Agent failed: {e}")

    # 5. WhatsApp Vecinos Agent
    if args.all or args.whatsapp:
        print("\n[Stage 4/6] Ingesting WhatsApp 'Chat de Vecinos' Stream...")
        try:
            wa_agent = WhatsAppVecinosAgent()
            wa_res = wa_agent.import_sample_condesa_chat()
            print(f" -> Completed: Ingested {len(wa_res)} hyper-local Vecinos problems.")
        except Exception as e:
            print(f" [Error] WhatsApp Agent failed: {e}")

    # 6. Mercado Libre Mexico Dual Intelligence Agent (Hot Products + Existing Product Problems)
    if args.all or args.mercadolibre or args.ml_hot or args.ml_problems:
        print("\n[Stage 5/6] Invoking Mercado Libre México Intelligence Agent...")
        try:
            ml_agent = MercadoLibreAgent()
            if args.ml_hot and not args.all:
                hot_items = ml_agent.get_hot_new_products()
                print(f" -> Displaying {len(hot_items)} Hot New Products & Breakout Trends on mercadolibre.com.mx:")
                for item in hot_items:
                    print(f"    * [{item.get('trend_badge')}] {item['title']} - ${item['price_mxn']:,.0f} MXN ({item.get('demand_growth')})")
            elif args.ml_problems and not args.all:
                problem_items = ml_agent.get_product_problems()
                print(f" -> Displaying {len(problem_items)} Existing Products with Severe Failure Modes & Complaints on mercadolibre.com.mx:")
                for item in problem_items:
                    print(f"    ! [{item.get('failure_mode')}] {item['title']} - Rating: {item['rating']}/5 ({len(item.get('reviews', []))} reviews)")
            else:
                ml_res = ml_agent.run()
                print(f" -> Completed: Harvested {ml_res['total_collected']} items ({ml_res.get('hot_new_products_count', 0)} Hot New Products, {ml_res.get('product_problems_count', 0)} Product Problems) from https://www.mercadolibre.com.mx/")
        except Exception as e:
            print(f" [Error] Mercado Libre Agent failed: {e}")

    # 7. Daily Report Generation
    if args.all or args.report:
        print("\n[Stage 6/6] Synthesizing Daily Bullet-Pointed Intelligence Report...")
        try:
            report_gen = DailyReportGenerator()
            report_res = report_gen.generate_report()
            print(f" -> Daily Report generated: {report_res['report_file']}")
        except Exception as e:
            print(f" [Error] Report Generation failed: {e}")

    # 6. Export Dataset
    if args.all or args.export:
        print("\n[Export] Generating fresh CSV & JSON dataset exports...")
        exports = db.export_dataset()
        print(f" -> CSV Export: {exports['csv_path']}")
        print(f" -> JSON Export: {exports['json_path']}")
        print(f" -> Total records exported: {exports['total_exported']}")

    print("\n" + "=" * 70)
    print(" EXECUTION COMPLETED SUCCESSFULLY")
    print(f" Metrics: {db.get_metrics()}")
    print("=" * 70)

if __name__ == "__main__":
    main()
