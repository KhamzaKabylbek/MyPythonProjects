def calculate_pozitivity_rate(P_bolen, P_poz_bolen, P_poz_ne_bolen):
    """
    Вычисление вероятности позитивного результата теста.
    
    Args:
        P_bolen (float): Вероятность того, что человек болен
        P_poz_bolen (float): Вероятность позитивного результата при болезни
        P_poz_ne_bolen (float): Вероятность ложнопозитивного результата
    
    Returns:
        float: Вероятность позитивного результата
    """
    return P_poz_bolen * P_bolen + P_poz_ne_bolen * (1 - P_bolen)



def main():
    # Параметры
    P_bolen = 0.1  # Вероятность того, что человек болен
    P_poz_bolen = 0.9  # Вероятность позитивного результата при болезни
    P_poz_ne_bolen = 0.1  # Вероятность ложнопозитивного результата

    # Вычисление P(позитивный результат)
    P_poz = calculate_pozitivity_rate(P_bolen, P_poz_bolen, P_poz_ne_bolen)

    # Применение теоремы Байеса
    P_bolen_given_poz = bayesian_theorem(P_bolen, P_poz)

    print(f"Вероятность болезни при позитивном результате теста: {P_bolen_given_poz:.4f}")

if __name__ == "__main__":
    main()
