import argparse
from markov.model import MarkovChain
from markov.utils import load_text, stream_train


def main():
    """ 
        python main.py --train big.txt --stream --order 2 --save model.pkl
        python main.py --load model.pkl --generate "the cat"  --length 100
        python main.py --train corpus.txt --generate "once upon"

    """
    parser = argparse.ArgumentParser(description="Markov Chain Text Generator")
    parser.add_argument("--train", help="Path to training text file")
    parser.add_argument("--stream", action="store_true", help="Stream large file")
    parser.add_argument("--order", type=int, default=2, help="Order of the markov chain")
    parser.add_argument("--save", help="Save trained model")
    parser.add_argument("--load", help="Load existing model")
    parser.add_argument("--generate", help="Text seed to start generation")
    parser.add_argument("--length", type=int, default=50, help="Generated text length")

    args = parser.parse_args()

    mc = MarkovChain(order=args.order)

    # Load model if provided
    if args.load:
        mc.load(args.load)
        print(f"Loaded model from {args.load}")

    # Train
    if args.train:
        if args.stream:
            print("Streaming training...")
            stream_train(args.train, mc)
        else:
            print("Loading full text...")
            text = load_text(args.train)
            mc.train(text)
        print("Training completed")

    # Save
    if args.save:
        mc.save(args.save)
        print(f"Saved mode to {args.save}")

    # Generate
    if args.generate:
        print("\nGenerated Text: \n")
        print(mc.generate(args.generate, args.length))


if __name__ == "__main__":
    main()