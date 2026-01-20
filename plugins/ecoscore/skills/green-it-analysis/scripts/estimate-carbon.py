#!/usr/bin/env python3
"""
Carbon footprint estimation calculator for software projects.
Usage: python estimate-carbon.py --tokens 1000000 --model large --region us-east-1
"""

import argparse
import json
import sys

# Carbon intensity by region (gCO2/kWh)
REGION_CARBON = {
    # AWS
    "eu-north-1": 8,
    "ca-central-1": 20,
    "us-west-2": 78,
    "eu-west-1": 316,
    "eu-central-1": 338,
    "us-east-1": 379,
    "us-east-2": 440,
    "ap-northeast-1": 506,
    "ap-southeast-1": 408,
    "ap-south-1": 708,
    # GCP
    "europe-north1": 96,
    "northamerica-northeast1": 20,
    "us-west1": 78,
    "us-central1": 440,
    # Azure
    "swedencentral": 8,
    "norwayeast": 19,
    "westus2": 78,
    "eastus": 379,
}

# CO2 per 1K tokens by model size (gCO2e)
MODEL_CARBON = {
    "small": 0.2,   # Haiku, GPT-3.5, etc.
    "medium": 0.5,  # Sonnet, GPT-4-mini
    "large": 1.2,   # Opus, GPT-4
}

# Server power consumption estimates (kWh per hour)
SERVER_POWER = {
    "small": 0.1,    # t3.micro equivalent
    "medium": 0.3,   # t3.large equivalent
    "large": 0.8,    # m5.xlarge equivalent
    "gpu": 2.5,      # GPU instance
}


def estimate_ai_carbon(tokens: int, model_size: str = "medium") -> dict:
    """Estimate carbon from AI/LLM usage."""
    carbon_per_1k = MODEL_CARBON.get(model_size, MODEL_CARBON["medium"])
    total_gco2 = (tokens / 1000) * carbon_per_1k

    return {
        "tokens": tokens,
        "model_size": model_size,
        "carbon_gco2": round(total_gco2, 2),
        "carbon_kg": round(total_gco2 / 1000, 4),
        "equivalent_km_driven": round(total_gco2 / 120, 2),  # avg car ~120g/km
    }


def estimate_server_carbon(
    hours: int,
    server_size: str = "medium",
    region: str = "us-east-1",
    count: int = 1
) -> dict:
    """Estimate carbon from server usage."""
    power_kwh = SERVER_POWER.get(server_size, SERVER_POWER["medium"])
    carbon_intensity = REGION_CARBON.get(region, 400)

    total_kwh = power_kwh * hours * count
    total_gco2 = total_kwh * carbon_intensity

    return {
        "hours": hours,
        "server_size": server_size,
        "server_count": count,
        "region": region,
        "region_carbon_intensity": carbon_intensity,
        "energy_kwh": round(total_kwh, 2),
        "carbon_gco2": round(total_gco2, 2),
        "carbon_kg": round(total_gco2 / 1000, 4),
    }


def estimate_build_carbon(
    build_minutes: int,
    builds_per_day: int = 10,
    region: str = "us-east-1"
) -> dict:
    """Estimate carbon from CI/CD builds."""
    # Assume build server uses ~0.5 kWh per hour
    hours_per_month = (build_minutes / 60) * builds_per_day * 30
    carbon_intensity = REGION_CARBON.get(region, 400)

    total_kwh = hours_per_month * 0.5
    total_gco2 = total_kwh * carbon_intensity

    return {
        "build_minutes": build_minutes,
        "builds_per_day": builds_per_day,
        "monthly_build_hours": round(hours_per_month, 1),
        "region": region,
        "monthly_carbon_gco2": round(total_gco2, 2),
        "monthly_carbon_kg": round(total_gco2 / 1000, 4),
    }


def get_region_recommendation(current_region: str) -> dict:
    """Recommend greener region alternatives."""
    current_carbon = REGION_CARBON.get(current_region, 400)
    greener_regions = [
        (region, carbon)
        for region, carbon in REGION_CARBON.items()
        if carbon < current_carbon
    ]
    greener_regions.sort(key=lambda x: x[1])

    savings = []
    for region, carbon in greener_regions[:3]:
        reduction = ((current_carbon - carbon) / current_carbon) * 100
        savings.append({
            "region": region,
            "carbon_intensity": carbon,
            "reduction_percent": round(reduction, 1)
        })

    return {
        "current_region": current_region,
        "current_carbon_intensity": current_carbon,
        "greener_alternatives": savings
    }


def main():
    parser = argparse.ArgumentParser(description="Estimate carbon footprint")
    parser.add_argument("--tokens", type=int, help="AI tokens consumed")
    parser.add_argument("--model", choices=["small", "medium", "large"], default="medium")
    parser.add_argument("--server-hours", type=int, help="Server hours")
    parser.add_argument("--server-size", choices=["small", "medium", "large", "gpu"], default="medium")
    parser.add_argument("--server-count", type=int, default=1)
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--build-minutes", type=int, help="Build time in minutes")
    parser.add_argument("--builds-per-day", type=int, default=10)
    parser.add_argument("--recommend-region", action="store_true")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    results = {}

    if args.tokens:
        results["ai_usage"] = estimate_ai_carbon(args.tokens, args.model)

    if args.server_hours:
        results["server_usage"] = estimate_server_carbon(
            args.server_hours, args.server_size, args.region, args.server_count
        )

    if args.build_minutes:
        results["build_usage"] = estimate_build_carbon(
            args.build_minutes, args.builds_per_day, args.region
        )

    if args.recommend_region:
        results["region_recommendation"] = get_region_recommendation(args.region)

    if not results:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for category, data in results.items():
            print(f"\n=== {category.replace('_', ' ').title()} ===")
            for key, value in data.items():
                if isinstance(value, list):
                    print(f"  {key}:")
                    for item in value:
                        print(f"    - {item}")
                else:
                    print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
