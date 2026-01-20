# Cloud Region Carbon Intensity

Carbon intensity data for major cloud provider regions.

## AWS Regions

| Region | Location | gCO2/kWh | Rating | Notes |
|--------|----------|----------|--------|-------|
| eu-north-1 | Stockholm, Sweden | 8 | Excellent | Hydro/nuclear powered |
| eu-west-1 | Ireland | 316 | Good | Wind investments |
| us-west-2 | Oregon | 78 | Good | Hydro heavy |
| ca-central-1 | Montreal | 20 | Excellent | Hydro powered |
| eu-central-1 | Frankfurt | 338 | Fair | Mixed grid |
| us-east-1 | N. Virginia | 379 | Fair | Coal/gas heavy |
| us-east-2 | Ohio | 440 | Poor | Coal heavy |
| ap-northeast-1 | Tokyo | 506 | Poor | Fossil heavy |
| ap-south-1 | Mumbai | 708 | Critical | Coal dominated |
| ap-southeast-1 | Singapore | 408 | Poor | Gas heavy |

## Google Cloud Regions

| Region | Location | gCO2/kWh | Rating |
|--------|----------|----------|--------|
| europe-north1 | Finland | 96 | Excellent |
| us-west1 | Oregon | 78 | Good |
| northamerica-northeast1 | Montreal | 20 | Excellent |
| europe-west1 | Belgium | 110 | Good |
| us-central1 | Iowa | 440 | Poor |
| asia-east1 | Taiwan | 509 | Poor |
| asia-south1 | Mumbai | 708 | Critical |

## Azure Regions

| Region | Location | gCO2/kWh | Rating |
|--------|----------|----------|--------|
| swedencentral | Sweden | 8 | Excellent |
| norwayeast | Norway | 19 | Excellent |
| canadacentral | Toronto | 20 | Excellent |
| westeurope | Netherlands | 328 | Fair |
| eastus | Virginia | 379 | Fair |
| westus2 | Washington | 78 | Good |
| southeastasia | Singapore | 408 | Poor |
| centralindia | Pune | 708 | Critical |

## Rating Scale

| Rating | gCO2/kWh Range | Recommendation |
|--------|----------------|----------------|
| Excellent | 0-50 | Preferred for all workloads |
| Good | 51-200 | Good choice, minor impact |
| Fair | 201-400 | Consider alternatives if latency allows |
| Poor | 401-600 | Avoid for non-latency-critical |
| Critical | 600+ | Only if absolutely required |

## Migration Recommendations

### Low-Latency Requirements

For applications requiring <50ms latency to users:
- Choose the greenest region within acceptable latency
- Consider edge computing for static content
- Use CDN to serve from green edge locations

### Batch Processing

For non-time-sensitive workloads:
- **Strongly prefer:** eu-north-1, ca-central-1, northamerica-northeast1
- Schedule during low-carbon grid periods
- Consider carbon-aware scheduling APIs

### Multi-Region Deployments

```
Primary: eu-north-1 (Sweden) - 8 gCO2/kWh
Failover: eu-west-1 (Ireland) - 316 gCO2/kWh
Edge CDN: Cloudflare/Fastly (optimized routing)
```

## Carbon-Aware Scheduling

### Time-of-Day Variations

Grid carbon intensity varies by time:
- **Low carbon:** Night (wind), Midday (solar in sunny regions)
- **High carbon:** Evening peak demand

### APIs for Real-Time Data

- **Electricity Maps API:** https://api.electricitymap.org
- **WattTime API:** https://api.watttime.org
- **Carbon Intensity UK:** https://carbonintensity.org.uk

### Implementation Pattern

```python
def get_greenest_region(regions: list[str]) -> str:
    """Select region with lowest current carbon intensity."""
    intensities = {
        region: get_carbon_intensity(region)
        for region in regions
    }
    return min(intensities, key=intensities.get)

def should_run_now(threshold_gco2: int = 200) -> bool:
    """Check if current grid carbon is below threshold."""
    current = get_current_carbon_intensity()
    return current < threshold_gco2
```

## Scoring Impact

### Infrastructure Score Adjustments

| Region Rating | Score Impact |
|---------------|--------------|
| Excellent | +10 points |
| Good | +5 points |
| Fair | 0 points |
| Poor | -10 points |
| Critical | -20 points |

### Detection Patterns

Look for region configuration in:
- `AWS_REGION` / `AWS_DEFAULT_REGION` env vars
- Terraform/CloudFormation region settings
- Kubernetes cluster configurations
- CDN configuration files
- Docker compose / deployment manifests

## Annual Carbon Comparison

For a typical web application (100 servers, 50% utilization):

| Region | Annual CO2e |
|--------|-------------|
| eu-north-1 | 3.5 tonnes |
| us-west-2 | 34 tonnes |
| us-east-1 | 166 tonnes |
| ap-south-1 | 310 tonnes |

**Potential savings:** Moving from ap-south-1 to eu-north-1 saves ~307 tonnes CO2e/year

## Data Sources

- AWS Sustainability: https://sustainability.aboutamazon.com
- Google Cloud Carbon: https://cloud.google.com/sustainability
- Azure Sustainability: https://azure.microsoft.com/sustainability
- Electricity Maps: https://app.electricitymap.org
- IEA Data: https://www.iea.org/data-and-statistics

**Note:** Carbon intensity values are approximate and vary seasonally. Use real-time APIs for accurate scheduling decisions.
