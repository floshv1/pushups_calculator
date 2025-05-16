if __name__ == "__main__":
    from pushups_calculator.gui import launch_app
    import argparse
    
    parser = argparse.ArgumentParser(description="Calculateur de Pompes League of Legends")
    parser.add_argument("--joueurs", type=int, default=1, help="Nombre de joueurs")
    args = parser.parse_args()

    launch_app(args.joueurs)
