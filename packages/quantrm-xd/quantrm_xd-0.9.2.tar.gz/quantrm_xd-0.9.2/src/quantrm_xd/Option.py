import numpy as np
from scipy.stats import norm
import inspect
from scipy.optimize import fsolve


def black_scholes(S0, K, T, r, q, sigma, option='call'):
    """
    Calculates the theoretical price of a European-style call or put option on a stock, using the Black-Scholes model.
    
    Parameters:
    - S0: the current stock price
    - K: the strike price of the option
    - T: the time to maturity of the option, expressed in years
    - r: the risk-free interest rate, expressed as a decimal
    - q: the continuously compounding coupon yield of the stock, expressed as a decimal
    - sigma: the implied volatility of the stock, expressed as a decimal
    - option: a string that indicates whether the option is a call or put option, default 'call'
    
    Returns:
    - price: the theoretical price of the option
    """
    
    d1 = (np.log(S0 / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option == 'call':
        price = S0 * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * np.exp(-q * T) * norm.cdf(-d1)
    
    return price

def implied_volatility_bs(S0, K, T, r, q, price, option='call'):
    """
    Solves for the implied volatility of a European-style call or put option on a stock, using the Black-Scholes model
    and the Newton-Raphson method.
    
    Parameters:
    - S0: the current stock price
    - K: the strike price of the option
    - T: the time to maturity of the option, expressed in years
    - r: the risk-free interest rate, expressed as a decimal
    - q: the continuously compounding coupon yield of the stock, expressed as a decimal
    - price: the market price of the option
    - option: a string that indicates whether the option is a call or put option, default 'call'
    
    Returns:
    - sigma: the implied volatility of the stock, expressed as a decimal
    """
    
    # Define a function to calculate the difference between the option price calculated
    # using the Black-Scholes model with a given value of sigma and the actual option price
    def error(sigma):
        return black_scholes(S0, K, T, r, q, sigma, option) - price
    
    # Define an initial guess for the implied volatility using the Black-Scholes model
    # with sigma=0.5
    sigma = 0.5
    
    # Set a maximum number of iterations and a tolerance level for the error
    max_iterations = 1000
    tolerance = 1e-6
    
    # Use the Newton-Raphson method to iteratively improve the guess for sigma
    for i in range(max_iterations):
        # Calculate the error for the current guess
        e = error(sigma)
        
        # If the error is small enough, exit the loop
        if abs(e) < tolerance:
            break
        
        # Calculate the derivative of the error with respect to sigma
        d = (error(sigma + 1e-6) - error(sigma)) / 1e-6
        
        # Update the guess for sigma using the Newton-Raphson formula
        sigma = sigma - e / d
    
    # Return the final value of sigma
    return sigma


class black_scholes_matrix:
    def __init__(self, S0, K, T, r, q, sigma, option='call'):
        """
        Initializes the Black-Scholes model with the given parameters.
        """
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.q = q
        self.sigma = sigma
        self.option = option
        
        self.d1 = (np.log(self.S0 / self.K) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        self.d2 = self.d1 - self.sigma * np.sqrt(self.T)
    
    def price(self):
        """
        Calculates the theoretical price of the option.
        """
        if self.option == 'call':
            price = self.S0 * np.exp(-self.q * self.T) * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        elif self.option == 'put':
            price = self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S0 * np.exp(-self.q * self.T) * norm.cdf(-self.d1)
        
        return price
    
    def delta(self):
        """
        Calculates the Delta of the option.
        """
        if self.option == 'call':
            delta = np.exp(-self.q * self.T) * norm.cdf(self.d1)
        elif self.option == 'put':
            delta = -np.exp(-self.q * self.T) * norm.cdf(-self.d1)
        
        return delta
    
    def gamma(self):
        """
        Calculates the Gamma of the option.
        """
        gamma = np.exp(-self.q * self.T) * norm.pdf(self.d1) / (self.S0 * self.sigma * np.sqrt(self.T))
        
        return gamma
    
    def vega(self):
        """
        Calculates the Vega of the option.
        """
        vega = self.S0 * np.exp(-self.q * self.T) * norm.pdf(self.d1) * np.sqrt(self.T)
        
        return vega
    
    def theta(self):
        """
        Calculates the Theta of the option.
        """
        if self.option == 'call':
            theta = -self.S0 * np.exp(-self.q * self.T) * norm.pdf(self.d1) * self.sigma / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2) + self.q * self.S0 * np.exp(-self.q * self.T) * norm.cdf(self.d1)
        elif self.option == 'put':
            theta = -self.S0 * np.exp(-self.q * self.T) * norm.pdf(self.d1) * self.sigma / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.q * self.S0 * np.exp(-self.q * self.T) * norm.cdf(-self.d1)
        
        return theta
    
    def rho(self):
        """
        Calculates the Rho of the option.
        """
        
        if self.option == 'call':
            rho = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        elif self.option == 'put':
            rho = -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2)

        return rho


    def carry_rho(self):
        """
        Calculates the Carry Rho of the option.
        """
        if self.option == 'call':
            carry_rho =  self.S0 * self.T * np.exp(-self.q * self.T) * norm.cdf(self.d1)
        elif self.option == 'put':
            carry_rho =  - self.S0 * self.T * np.exp(-self.q * self.T) * norm.cdf(-self.d1)

        return carry_rho

    
    def greeks(self):
        """
        Calculates and returns all the greeks of the option as a dictionary.
        """
        value = self.price()
        delta = self.delta()
        gamma = self.gamma()
        vega = self.vega()
        theta = self.theta()
        rho = self.rho()
        carry_rho = self.carry_rho()
        
        return {'Value': value, 'Delta': delta, 'Gamma': gamma, 'Vega': vega, 'Theta': theta, 'Rho': rho, "Carry Rho": carry_rho}
    


def binomial_tree_american_continous(S0, K, T, r, q, sigma, N=200, option_type='call'):
    dt = T/N
    u = np.exp(sigma*np.sqrt(dt))
    d = 1/u
    pu = (np.exp((r-q)*dt)-d)/(u-d)
    pd = 1-pu
    df = np.exp(-r*dt)
    z = 1 if option_type == 'call' else -1
    def nNodeFunc(n):
        return (n+2)*(n+1)//2
    def idxFunc(i,j):
        return nNodeFunc(j-1)+i
    nNodes = nNodeFunc(N)
    optionValues = np.empty(nNodes, dtype = float)

    for j in range(N, -1, -1):
        for i in range(j, -1, -1):
            idx = idxFunc(i,j)
            price = S0*u**i*d**(j-i)
            optionValues[idx] = max(0,z*(price-K))
            if j < N:
                optionValues[idx] = max(optionValues[idx], df*(pu*optionValues[idxFunc(i+1,j+1)] + pd*optionValues[idxFunc(i,j+1)])  )
    return optionValues[0]


def binomial_tree_american_discrete(S0, K, r, T, sigma, N, option_type, dividend_dates=None, dividend_amounts=None):
    if dividend_dates is None or dividend_amounts is None or (len(dividend_amounts)==0) or (len(dividend_dates)==0):
        return binomial_tree_american_continous(S0, K, T, r, 0, sigma, N, option_type)
    elif dividend_dates[0] > N:
        return binomial_tree_american_continous(S0, K, T, r, 0, sigma, N, option_type)

    dt = T/N
    u = np.exp(sigma*np.sqrt(dt))
    d = 1/u
    pu = (np.exp(r*dt)-d)/(u-d)
    pd = 1-pu
    df = np.exp(-r*dt)
    z = 1 if option_type == 'call' else -1
    
    def nNodeFunc(n):
        return (n+2)*(n+1)//2
    def idxFunc(i,j):
        return nNodeFunc(j-1)+i
   
    nDiv = len(dividend_dates)
    nNodes = nNodeFunc(dividend_dates[0])

    optionValues = np.empty(nNodes, dtype = float)

    for j in range(dividend_dates[0],-1,-1):
        for i in range(j,-1,-1):
            idx = idxFunc(i,j)
            price = S0*u**i*d**(j-i)       
            
            if j < dividend_dates[0]:
                #times before the dividend working backward induction
                optionValues[idx] = max(0,z*(price-K))
                optionValues[idx] = max(optionValues[idx], df*(pu*optionValues[idxFunc(i+1,j+1)] + pd*optionValues[idxFunc(i,j+1)])  )
                
            else:
                no_ex= binomial_tree_american_discrete(price-dividend_amounts[0], K, r, T-dividend_dates[0]*dt, sigma, N-dividend_dates[0], option_type, [x- dividend_dates[0] for x in dividend_dates[1:nDiv]], dividend_amounts[1:nDiv] )
                ex =  max(0,z*(price-K))
                optionValues[idx] = max(no_ex,ex)

    return optionValues[0]

def implied_volatility_bt(S0, K, r, T, price, N, option, dividend_dates=None, dividend_amounts=None):
    f1 = lambda z: (binomial_tree_american_discrete(S0, K, r, T, z, N, option, dividend_dates, dividend_amounts)-price)
    return fsolve(f1, x0 = 0.2)[0]


# calculate first order derivative
def first_order_der(func, x, delta):
    return (func(x * (1 + delta)) - func(x * (1 - delta))) / (2 * x * delta)

# calculate second order derivative
def second_order_der(func, x, delta):
    return (func(x * (1 + delta)) + func(x * (1 - delta)) - 2 * func(x)) / (x * delta) ** 2

def cal_partial_derivative(func, order, arg_name, delta=1e-5):
  # initialize for argument names and order
    arg_names = list(inspect.signature(func).parameters.keys())
    derivative_fs = {1: first_order_der, 2: second_order_der}

    def partial_derivative(*args, **kwargs):
        # parse argument names and order
        args_dict = dict(list(zip(arg_names, args)) + list(kwargs.items()))
        arg_val = args_dict.pop(arg_name)

        def partial_f(x):
            p_kwargs = {arg_name:x, **args_dict}
            return func(**p_kwargs)
        return derivative_fs[order](partial_f, arg_val, delta)
    return partial_derivative


class OptionGreekCalculator:
    def __init__(self, option_price_func, S, K, r, T, sigma, option_type, q = None, N = None, dividend_dates=None, dividend_amounts=None):
        self.option_price_func = option_price_func
        self.S = S
        self.K = K
        self.r = r
        self.q = q
        self.T = T
        self.sigma = sigma
        self.N = N
        self.option_type = option_type
        self.dividend_dates = dividend_dates
        self.dividend_amounts = dividend_amounts
        
    def __call__(self, *args, **kwargs):
        return self.option_price_func(*args, **kwargs)
    
    def delta(self):
        delta_calculator = cal_partial_derivative(self.option_price_func, 1, 'S0')
        if self.option_price_func == black_scholes:
            delta = delta_calculator(self.S, self.K, self.r, self.q, self.T, self.sigma, self.option_type)
        elif self.option_price_func == binomial_tree_american_continous:
            delta = delta_calculator(self.S, self.K, self.T, self.r, self.q, self.sigma, self.N, self.option_type)
        elif self.option_price_func == binomial_tree_american_discrete:
            delta = delta_calculator(self.S, self.K, self.r, self.T, self.sigma, self.N, self.option_type, self.dividend_dates, self.dividend_amounts)
        return delta
    
    def gamma(self):
        gamma_calculator = cal_partial_derivative(self.option_price_func, 2, 'S0')
        if self.option_price_func == black_scholes:
            gamma = gamma_calculator(self.S, self.K, self.r, self.q, self.T, self.sigma, self.option_type)
        elif self.option_price_func == binomial_tree_american_continous:
            gamma = gamma_calculator(self.S, self.K, self.T, self.r, self.q, self.sigma, self.N, self.option_type)
        elif self.option_price_func == binomial_tree_american_discrete:
            gamma = gamma_calculator(self.S, self.K, self.r, self.T, self.sigma, self.N, self.option_type, self.dividend_dates, self.dividend_amounts)
        return gamma
    
    def vega(self):
        vega_calculator = cal_partial_derivative(self.option_price_func, 1, 'sigma')
        if self.option_price_func == black_scholes:
            vega = vega_calculator(self.S, self.K, self.r, self.q, self.T, self.sigma, self.option_type)
        elif self.option_price_func == binomial_tree_american_continous:
            vega = vega_calculator(self.S, self.K, self.T, self.r, self.q, self.sigma, self.N, self.option_type)
        elif self.option_price_func == binomial_tree_american_discrete:
            vega = vega_calculator(self.S, self.K, self.r, self.T, self.sigma, self.N, self.option_type, self.dividend_dates, self.dividend_amounts)
        return vega
    
    def theta(self):
        theta_calculator = cal_partial_derivative(self.option_price_func, 1, 'T')
        if self.option_price_func == black_scholes:
            theta = theta_calculator(self.S, self.K, self.r, self.q, self.T, self.sigma, self.option_type)
        elif self.option_price_func == binomial_tree_american_continous:
            theta = theta_calculator(self.S, self.K, self.T, self.r, self.q, self.sigma, self.N, self.option_type)
        elif self.option_price_func == binomial_tree_american_discrete:
            theta = theta_calculator(self.S, self.K, self.r, self.T, self.sigma, self.N, self.option_type, self.dividend_dates, self.dividend_amounts)
        return -theta
    
    def rho(self):
        rho_calculator = cal_partial_derivative(self.option_price_func, 1, 'r')
        if self.option_price_func == black_scholes:
            rho = rho_calculator(self.S, self.K, self.r, self.q, self.T, self.sigma, self.option_type)
        elif self.option_price_func == binomial_tree_american_continous:
            rho = rho_calculator(self.S, self.K, self.T, self.r, self.q, self.sigma, self.N, self.option_type)
        elif self.option_price_func == binomial_tree_american_discrete:
            rho = rho_calculator(self.S, self.K, self.r, self.T, self.sigma, self.N, self.option_type, self.dividend_dates, self.dividend_amounts)
        return rho 
    
    def carry_rho(self):
        carry_rho_calculator = cal_partial_derivative(self.option_price_func, 1, 'q')
        if self.option_price_func == black_scholes:
            carry_rho = self.rho() - carry_rho_calculator(self.S, self.K, self.r, self.q, self.T, self.sigma, self.option_type)
        elif self.option_price_func == binomial_tree_american_continous:
            carry_rho = self.rho() - carry_rho_calculator(self.S, self.K, self.T, self.r, self.q, self.sigma, self.N, self.option_type)
        elif self.option_price_func == binomial_tree_american_discrete:
            return
        return carry_rho 
    
    def sensitivity_to_dividend(self):
        if self.dividend_dates is None or self.dividend_amounts is None or self.option_price_func != binomial_tree_american_discrete:
            return
        delta = 1e-3
        div_amounts_1 = [self.dividend_amounts[0]+delta] + self.dividend_amounts[1:]
        div_amounts_2 = [self.dividend_amounts[0]-delta] + self.dividend_amounts[1:]
        V1 = binomial_tree_american_discrete(self.S, self.K, self.r, self.T, self.sigma, self.N, self.option_type, self.dividend_dates, div_amounts_1)    
        V2 = binomial_tree_american_discrete(self.S, self.K, self.r, self.T, self.sigma, self.N, self.option_type, self.dividend_dates, div_amounts_2)    
        sensitivity_to_dividend = (V1 - V2) / (2*delta)
        return sensitivity_to_dividend
    
    def greeks(self):
        delta = self.delta()
        gamma = self.gamma()
        vega = self.vega()
        theta = self.theta()
        rho = self.rho()
        carry_rho = self.carry_rho() 
        sensitivity_to_dividend = self.sensitivity_to_dividend()
        
        return {'Delta': delta, 'Gamma': gamma, 'Vega': vega, 'Theta': theta, 'Rho': rho, "Carry Rho": carry_rho, "Senstivity to Dividend": sensitivity_to_dividend}