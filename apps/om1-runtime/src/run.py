#!/usr/bin/env python3
"""
Bitcoin Advisor Agent Runtime Entry Point

Custom lightweight agent runtime inspired by OM1 patterns.
Tailored for financial trading applications.
"""

import sys
import json
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agent.runtime import BitcoinAdvisorAgent


def load_config(config_name: str) -> dict:
    """
    Load agent configuration from JSON file.

    Args:
        config_name: Name of config file (without .json extension)

    Returns:
        Configuration dict

    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    config_path = project_root / 'config' / f'{config_name}.json'

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Replace environment variable placeholders
    config_str = json.dumps(config)
    for key, value in os.environ.items():
        config_str = config_str.replace(f'${{{key}}}', value)

    return json.loads(config_str)


def main():
    """Main entry point for Bitcoin Advisor agent runtime."""
    # Load environment variables from root directory (two levels up)
    env_path = project_root.parent.parent / '.env'
    load_dotenv(env_path)

    parser = argparse.ArgumentParser(
        description='Bitcoin Advisor Agent Runtime - Lightweight trading agent inspired by OM1'
    )
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'status'],
        help='Command to execute'
    )
    parser.add_argument(
        'config_name',
        nargs='?',
        default='bitcoin_advisor',
        help='Configuration file name (without .json extension)'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level'
    )
    parser.add_argument(
        '--log-to-file',
        action='store_true',
        help='Log to file instead of console'
    )
    parser.add_argument(
        '--cycles',
        type=int,
        help='Number of cycles to run (default: infinite)'
    )

    args = parser.parse_args()

    if args.command == 'start':
        try:
            # Load configuration
            print(f"📋 Loading configuration: {args.config_name}.json")
            config = load_config(args.config_name)
            print(f"✅ Configuration loaded\n")

            # Initialize agent
            agent = BitcoinAdvisorAgent(config)

            # Run agent
            if args.cycles:
                print(f"🔢 Running for {args.cycles} cycles...")
                for _ in range(args.cycles):
                    agent.run_cycle()
                print(f"✅ Completed {args.cycles} cycles")
            else:
                agent.run()

        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            return 1
        except KeyboardInterrupt:
            print("\n\n🛑 Agent stopped by user")
            return 0
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
            return 1

    elif args.command == 'stop':
        print("🛑 Stopping agent...")
        print("⚠️  Stop command not yet implemented (use Ctrl+C to stop running agent)")
        return 0

    elif args.command == 'status':
        print("📊 Agent Status: Not Running")
        print("⚠️  Status command not yet implemented")
        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
