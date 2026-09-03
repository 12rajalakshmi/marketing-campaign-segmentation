import csv
import os


# ---------------------------------------------------------
# LEAD SCORING SYSTEM
# ---------------------------------------------------------

INPUT_FILE = "leads.csv"
OUTPUT_FILE = "scored_leads.csv"


def calculate_score(lead):
    """
    Calculate the lead score based on customer behavior
    and interest.
    """

    score = 0

    # -----------------------------------------------------
    # Website visit
    # -----------------------------------------------------
    if lead["website_visit"].lower() == "yes":
        score += 15

    # -----------------------------------------------------
    # WhatsApp reply
    # -----------------------------------------------------
    if lead["whatsapp_reply"].lower() == "yes":
        score += 20

    # -----------------------------------------------------
    # Service interest
    # -----------------------------------------------------
    service_interest = lead["service_interest"].lower()

    if service_interest == "high":
        score += 30

    elif service_interest == "medium":
        score += 20

    elif service_interest == "low":
        score += 5

    # -----------------------------------------------------
    # Budget
    # -----------------------------------------------------
    budget = lead["budget"].lower()

    if budget == "high":
        score += 35

    elif budget == "medium":
        score += 20

    elif budget == "low":
        score += 5

    return score


def classify_lead(score):
    """
    Convert score into Hot, Warm or Cold lead.
    """

    if score >= 70:
        return "Hot"

    elif score >= 40:
        return "Warm"

    else:
        return "Cold"


def read_leads():
    """
    Read lead information from the CSV file.
    """

    leads = []

    try:

        with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:
                leads.append(row)

    except FileNotFoundError:

        print(f"ERROR: {INPUT_FILE} was not found.")
        print("Please make sure leads.csv is inside the project folder.")

    return leads


def score_leads(leads):
    """
    Calculate score and classification for every lead.
    """

    scored_leads = []

    for lead in leads:

        score = calculate_score(lead)

        category = classify_lead(score)

        lead["score"] = score
        lead["category"] = category

        scored_leads.append(lead)

    return scored_leads


def save_results(scored_leads):
    """
    Save scored leads into a new CSV file.
    """

    if not scored_leads:
        print("No leads available to save.")
        return

    fieldnames = [
        "name",
        "email",
        "age",
        "source",
        "website_visit",
        "whatsapp_reply",
        "service_interest",
        "budget",
        "score",
        "category"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(scored_leads)

    print()
    print(f"Results saved successfully to: {OUTPUT_FILE}")


def display_results(scored_leads):
    """
    Display lead scoring results in the terminal.
    """

    print()
    print("=" * 70)
    print("              MARKETING LEAD SCORING RESULTS")
    print("=" * 70)

    print(
        f"{'Name':<15}"
        f"{'Source':<12}"
        f"{'Score':<10}"
        f"{'Category':<10}"
    )

    print("-" * 70)

    for lead in scored_leads:

        print(
            f"{lead['name']:<15}"
            f"{lead['source']:<12}"
            f"{lead['score']:<10}"
            f"{lead['category']:<10}"
        )

    print("=" * 70)


def display_summary(scored_leads):
    """
    Display Hot, Warm and Cold lead counts.
    """

    hot = 0
    warm = 0
    cold = 0

    for lead in scored_leads:

        if lead["category"] == "Hot":
            hot += 1

        elif lead["category"] == "Warm":
            warm += 1

        elif lead["category"] == "Cold":
            cold += 1

    total = len(scored_leads)

    print()
    print("=" * 50)
    print("                 LEAD SUMMARY")
    print("=" * 50)

    print(f"Total Leads : {total}")
    print(f"Hot Leads   : {hot}")
    print(f"Warm Leads  : {warm}")
    print(f"Cold Leads  : {cold}")

    print("=" * 50)


def display_hot_leads(scored_leads):
    """
    Display only Hot Leads.
    """

    print()
    print("=" * 70)
    print("                    HOT LEADS")
    print("=" * 70)

    hot_found = False

    for lead in scored_leads:

        if lead["category"] == "Hot":

            hot_found = True

            print(
                f"Name   : {lead['name']}\n"
                f"Email  : {lead['email']}\n"
                f"Source : {lead['source']}\n"
                f"Score  : {lead['score']}\n"
            )

    if not hot_found:
        print("No hot leads found.")

    print("=" * 70)


def display_source_summary(scored_leads):
    """
    Show how many leads came from each marketing source.
    """

    sources = {}

    for lead in scored_leads:

        source = lead["source"]

        if source not in sources:
            sources[source] = 0

        sources[source] += 1

    print()
    print("=" * 50)
    print("             MARKETING SOURCE SUMMARY")
    print("=" * 50)

    for source, count in sources.items():

        print(f"{source:<20} {count} leads")

    print("=" * 50)


def main():

    print()
    print("=" * 70)
    print("          MARKETING CAMPAIGN LEAD SCORING SYSTEM")
    print("=" * 70)

    # Check whether input file exists
    if not os.path.exists(INPUT_FILE):

        print()
        print(f"ERROR: {INPUT_FILE} does not exist.")
        print("Create leads.csv in the project folder.")
        return

    # Step 1: Read leads
    print()
    print("Step 1: Reading leads from CSV...")

    leads = read_leads()

    if not leads:

        print("No leads found.")
        return

    print(f"{len(leads)} leads loaded successfully.")

    # Step 2: Score leads
    print()
    print("Step 2: Calculating lead scores...")

    scored_leads = score_leads(leads)

    print("Lead scoring completed.")

    # Step 3: Display results
    print()
    print("Step 3: Displaying results...")

    display_results(scored_leads)

    # Step 4: Display summary
    display_summary(scored_leads)

    # Step 5: Display hot leads
    display_hot_leads(scored_leads)

    # Step 6: Marketing source summary
    display_source_summary(scored_leads)

    # Step 7: Save results
    print()
    print("Step 4: Saving results...")

    save_results(scored_leads)

    print()
    print("=" * 70)
    print("                  PROCESS COMPLETED")
    print("=" * 70)


# ---------------------------------------------------------
# START PROGRAM
# ---------------------------------------------------------

if __name__ == "__main__":
    main()