import matplotlib.pyplot as plt


probs = {
    "C": 1/100,
    "D|C": 99/100,
    "D|!C": 5/100
}


def p_from_kb(of):
    """A simple probability from the knowledge base."""
    if of in probs:
        return probs[of]
    if of.startswith("!"):
        return 1 - p_from_kb(of[1:])
    # For anything in the DB of the form 'of|x' or '!of|x',
    # for which we can calculate p_from_kb(x).
    return sum(probs[k] for k
    )


def posterior(of, given):
    """Posterior probability from Bayes' rule."""
    prior = probs[of]
    print(f"Prior P({of}) = {prior}")
    likelihood = 


if __name__ == "__main__":
    posterior(of="C")
