if __name__ == "__main__":
    from gui import run
    import argparse
    
    parser = argparse.ArgumentParser(description="Calculateur de Pompes League of Legends")
    parser.add_argument("--joueurs", type=int, default=2, help="Nombre de joueurs")
    args = parser.parse_args()

    run(args.joueurs)
