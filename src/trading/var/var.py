import numpy as np


def cent_loss(operation_range:int=2000, lotaje: float=0.01, operation_number:int=40):
    "return the loss in dolas for a cent account"
    average = (operation_range/operation_number)
    loss = 0
    for i in range(0, operation_number - 1):
        loss += (operation_range - i*average)*lotaje / 10
    return loss


def get_operation_num(capital:float=80000, lotaje:int=0.02, min_marging:int =10000, palanca:int=500, valor_activo:float=4720):
    
    
    margin = (valor_activo*100 * lotaje) / palanca
    operations = int(((capital / margin) * 100) / min_marging)

    return operations


def get_operation_range(operation_number:int = 40, averages:int=50):
    """
    description:
        funtion to get operation range given the number of operation 
    return:
        the operation range in number of pips
    """
    return operation_number * averages


def calcular_retornos(datos):
    """
    Calcula los retornos diarios  del oro
    """
    
    retornos = datos['Close']['GC=F'].pct_change() 
    retornos = retornos.dropna()
    return retornos


def historical_var_percentiles(returns, lower_pct: float = 5.0, upper_pct: float = 95.0) -> dict:
    """
    Calculate historical VaR percentiles for gold daily returns.

    Uses empirical distribution (no normality assumption), suited for gold
    which exhibits fat tails and skewness.

    Parameters:
    - returns: daily percentage returns (from calcular_retornos)
    - lower_pct: downside percentile, e.g. 5.0 means worst 5% of days
    - upper_pct: upside percentile, e.g. 95.0 means best 95% of days

    Returns dict with:
    - lower_var: daily loss at the lower percentile (negative = loss)
    - upper_var: daily gain at the upper percentile (positive = gain)
    - lower_pct / upper_pct: the requested percentiles
    - worst_day / best_day: the single worst and best daily move observed
    - mean / std: descriptive stats of the return distribution
    """
    r = np.asarray(returns)
    return {
        'lower_pct': lower_pct,
        'upper_pct': upper_pct,
        'lower_var': float(np.percentile(r, lower_pct)),
        'upper_var': float(np.percentile(r, upper_pct)),
        'worst_day': float(r.min()),
        'best_day': float(r.max()),
        'mean': float(r.mean()),
        'std': float(r.std()),
    }


def expected_shortfall(returns, lower_pct: float = 5.0) -> float:
    """
    Average loss on the days beyond the lower_pct threshold (CVaR/ES).
    More conservative than VaR alone — captures tail severity, not just the cut-off.
    """
    r = np.asarray(returns)
    threshold = np.percentile(r, lower_pct)
    tail = r[r <= threshold]
    return float(tail.mean())




