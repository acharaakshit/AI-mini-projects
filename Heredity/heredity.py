import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    prob = 1
    for person, data in people.items():
        if person in one_gene:
            if data["mother"] is None:
                # if there is no parent, directly use the probability
                prob = prob * PROBS["gene"][1]
            # if person gets one copy of gene from one parent and 0 from other
            elif data["mother"] in two_genes and data["father"] in two_genes:
                prob = prob * 2 * (1 - PROBS["mutation"]) * PROBS["mutation"]
            elif (data["mother"] in two_genes or data["father"] in two_genes) and (data["mother"] in one_gene or data["father"] in one_gene):
                prob = prob * ((1 - PROBS["mutation"]) * (0.5 + PROBS["mutation"]) + PROBS["mutation"] * (0.5 - PROBS["mutation"]))
            elif data["father"] in one_gene and data["mother"] in one_gene:
                prob = prob * 2 * (0.5 - PROBS["mutation"]) * (0.5 + PROBS["mutation"])
            elif (data["father"] not in one_gene and data["father"] not in two_genes) or (data["mother"] not in one_gene and data["mother"] not in two_genes):
                if data["father"] in one_gene or data["mother"] in one_gene:
                    prob = prob * (0.5 - PROBS["mutation"]) * (1 - PROBS["mutation"])
                elif data["mother"] in two_genes or data["father"] in two_genes:
                    prob = prob * 2 * (1 - PROBS["mutation"]) * PROBS["mutation"]
                else:
                    prob = prob * 2 * (1 - PROBS["mutation"]) * PROBS["mutation"]
            # choose the probability according to whether the person has a trait or not
            if person in have_trait:
                prob = prob * PROBS["trait"][1][True]
            else:
                prob = prob * PROBS["trait"][1][False]

        elif person in two_genes:
            if data["mother"] is None:
                prob = prob * PROBS["gene"][2]
            # if the person gets one copy of the gene from each parent
            elif data["mother"] in two_genes and data["father"] in two_genes:
                prob = prob * pow(1 - PROBS["mutation"], 2)
            elif (data["mother"] in two_genes or data["father"] in two_genes) and (data["mother"] in one_gene or data["father"] in one_gene):
                prob = prob * (1- PROBS["mutation"]) * (0.5 - PROBS["mutation"])
            elif data["father"] in one_gene and data["mother"] in one_gene:
                prob = prob * pow(0.5 - PROBS["mutation"], 2)
            elif (data["father"] not in one_gene and data["father"] not in two_genes) or (data["mother"] not in one_gene and data["mother"] not in two_genes):
                if data["father"] in one_gene or data["mother"] in one_gene:
                    prob = prob * (0.5 - PROBS["mutation"]) * PROBS["mutation"]
                elif data["mother"] in two_genes or data["father"] in two_genes:
                    prob = prob * (1- PROBS["mutation"]) * PROBS["mutation"]
                else:
                    prob = prob * PROBS["mutation"] * PROBS["mutation"]
            if person in have_trait:
                prob = prob * PROBS["trait"][2][True]
            else:
                prob = prob * PROBS["trait"][2][False]

        else:
            if data["mother"] is None:
                prob = prob * PROBS["gene"][0]
            # if the person gets 0 copies of the gene from each parent
            elif data["mother"] in two_genes and data["father"] in two_genes:
                prob = prob * pow(PROBS["mutation"], 2)
            elif (data["mother"] in two_genes or data["father"] in two_genes) and (data["mother"] in one_gene or data["father"] in one_gene):
                prob = prob *  PROBS["mutation"] * (0.5 + PROBS["mutation"])
            elif data["father"] in one_gene and data["mother"] in one_gene:
                prob = prob * pow(0.5 + PROBS["mutation"], 2)
            elif (data["father"] not in one_gene and data["father"] not in two_genes) or (data["mother"] not in one_gene and data["mother"] not in two_genes):
                if data["father"] in one_gene or data["mother"] in one_gene:
                    prob = prob * (0.5 + PROBS["mutation"]) * (1 - PROBS["mutation"])
                elif data["mother"] in two_genes or data["father"] in two_genes:
                    prob = prob * PROBS["mutation"] * (1 - PROBS["mutation"])
                else:
                    prob = prob * (1 - PROBS["mutation"]) * (1- PROBS["mutation"])
            if person in have_trait:
                prob = prob * PROBS["trait"][0][True]
            else:
                prob = prob * PROBS["trait"][0][False]

    return prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for key, value in probabilities.items():
        # update the probability that the person has x copies of gene by adding the joint probability p
        if key in one_gene:
            probabilities[key]["gene"][1] = probabilities[key]["gene"][1] + p
        elif key in two_genes:
            probabilities[key]["gene"][2] = probabilities[key]["gene"][2] + p
        else:
            probabilities[key]["gene"][0] = probabilities[key]["gene"][0] + p

        # update the probability that the person exhibits a trait by adding the joint probability p
        if key in have_trait:
            probabilities[key]["trait"][True] = probabilities[key]["trait"][True] + p
        else:
            probabilities[key]["trait"][False] = probabilities[key]["trait"][False] + p




def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for key, value in probabilities.items():
        # normalize the genes
        tot_prob_gene = value["gene"][0] + value["gene"][1] + value["gene"][2]
        value["gene"][0] = value["gene"][0]/tot_prob_gene
        value["gene"][1] = value["gene"][1]/ tot_prob_gene
        value["gene"][2] = value["gene"][2]/tot_prob_gene

        # normalize the traits
        tot_prob_trait = value["trait"][True] + value["trait"][False]
        value["trait"][True] = value["trait"][True]/tot_prob_trait
        value["trait"][False] =value["trait"][False]/tot_prob_trait


if __name__ == "__main__":
    main()
