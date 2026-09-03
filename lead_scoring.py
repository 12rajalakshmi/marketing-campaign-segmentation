import csv
import os


# =========================================================
# MARKETING CAMPAIGN LEAD SCORING SYSTEM
# =========================================================

INPUT_FILE = "leads.csv"
OUTPUT_FILE = "scored_leads.csv"


# =========================================================
# 1. CALCULATE LEAD SCORE
# =========================================================

def calculate_score(lead):
    """
    Calculate the lead score based on customer behavior,
    service interest, and budget.
    """

    score = 0

    # Website visit
    if lead["website_visit"].lower() == "yes":
        score += 15

    # WhatsApp reply
    if lead["whatsapp_reply"].lower() == "yes":
        score += 20

    # Service interest
    service_interest = lead["service_interest"].lower()

    if service_interest == "high":
        score += 30

    elif service_interest == "medium":
        score += 20

    elif service_interest == "low":
        score += 5

    # Budget
    budget = lead["budget"].lower()

    if budget == "high":
        score += 35

    elif budget == "medium":
        score += 20

    elif budget == "low":
        score += 5

    return score


# =========================================================
# 2. CLASSIFY LEAD
# =========================================================

def classify_lead(score):
    """
    Classify leads as Hot, Warm, or Cold.
    """

    if score >= 70:
        return "Hot"

    elif score >= 40:
        return "Warm"

    else:
        return "Cold"


# =========================================================
# 3. GET MARKETING ACTION
# =========================================================

def get_marketing_action(category):
    """
    Recommend the next marketing action based on
    the lead category.
    """

    if category == "Hot":
        return "Call immediately"

    elif category == "Warm":
        return "Send WhatsApp follow-up"

    else:
        return "Add to remarketing"


# =========================================================
# 4. READ LEADS FROM CSV
# =========================================================

def read_leads():
    """
    Read customer leads from leads.csv.
    """

    leads = []

    try:

        with open(
            INPUT_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                leads.append(row)

    except FileNotFoundError:

        print()
        print("ERROR")
        print("-" * 50)
        print(f"{INPUT_FILE} was not found.")
        print("Please make sure leads.csv is inside the project folder.")
        print("-" * 50)

    return leads


# =========================================================
# 5. SCORE ALL LEADS
# =========================================================

def score_leads(leads):
    """
    Calculate score, category, and marketing action
    for every lead.
    """

    scored_leads = []

    for lead in leads:

        # Calculate score
        score = calculate_score(lead)

        # Classify lead
        category = classify_lead(score)

        # Get recommended action
        action = get_marketing_action(category)

        # Add new information
        lead["score"] = score
        lead["category"] = category
        lead["marketing_action"] = action

        scored_leads.append(lead)

    return scored_leads


# =========================================================
# 6. DISPLAY LEAD RESULTS
# =========================================================

def display_results(scored_leads):
    """
    Display all lead scoring results.
    """

    print()
    print("=" * 90)
    print("                 MARKETING LEAD SCORING RESULTS")
    print("=" * 90)

    print(
        f"{'Name':<15}"
        f"{'Source':<12}"
        f"{'Score':<10}"
        f"{'Category':<12}"
        f"{'Action':<30}"
    )

    print("-" * 90)

    for lead in scored_leads:

        print(
            f"{lead['name']:<15}"
            f"{lead['source']:<12}"
            f"{lead['score']:<10}"
            f"{lead['category']:<12}"
            f"{lead['marketing_action']:<30}"
        )

    print("=" * 90)


# =========================================================
# 7. DISPLAY SUMMARY
# =========================================================

def display_summary(scored_leads):
    """
    Display total Hot, Warm, and Cold leads.
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
    print("                    LEAD SUMMARY")
    print("=" * 50)

    print(f"Total Leads : {total}")
    print(f"Hot Leads   : {hot}")
    print(f"Warm Leads  : {warm}")
    print(f"Cold Leads  : {cold}")

    print("=" * 50)


# =========================================================
# 8. DISPLAY HOT LEADS
# =========================================================

def display_hot_leads(scored_leads):
    """
    Display all Hot Leads that require immediate attention.
    """

    print()
    print("=" * 70)
    print("                         HOT LEADS")
    print("=" * 70)

    hot_found = False

    for lead in scored_leads:

        if lead["category"] == "Hot":

            hot_found = True

            print()
            print(f"Name   : {lead['name']}")
            print(f"Email  : {lead['email']}")
            print(f"Source : {lead['source']}")
            print(f"Score  : {lead['score']}")
            print(f"Action : {lead['marketing_action']}")
            print("-" * 70)

    if not hot_found:
        print("No Hot Leads found.")

    print("=" * 70)


# =========================================================
# 9. DISPLAY MARKETING SOURCE SUMMARY
# =========================================================

def display_source_summary(scored_leads):
    """
    Show the number of leads generated by each
    marketing source.
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


# =========================================================
# 10. DISPLAY MARKETING ACTIONS
# =========================================================

def display_marketing_actions(scored_leads):
    """
    Display the recommended marketing action
    for every lead.
    """

    print()
    print("=" * 90)
    print("                    MARKETING ACTIONS")
    print("=" * 90)

    print(
        f"{'Name':<15}"
        f"{'Score':<10}"
        f"{'Category':<12}"
        f"{'Recommended Action':<35}"
    )

    print("-" * 90)

    for lead in scored_leads:

        print(
            f"{lead['name']:<15}"
            f"{lead['score']:<10}"
            f"{lead['category']:<12}"
            f"{lead['marketing_action']:<35}"
        )

    print("=" * 90)


# =========================================================
# 11. SAVE RESULTS TO CSV
# =========================================================

def save_results(scored_leads):
    """
    Save the scored leads into scored_leads.csv.
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
        "category",
        "marketing_action"
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
    print(f"Results successfully saved to: {OUTPUT_FILE}")


# =========================================================
# 12. MAIN PROGRAM
# =========================================================

def main():

    print()
    print("=" * 90)
    print("          MARKETING CAMPAIGN LEAD SCORING SYSTEM")
    print("=" * 90)

    # -----------------------------------------------------
    # Check input file
    # -----------------------------------------------------

    if not os.path.exists(INPUT_FILE):

        print()
        print(f"ERROR: {INPUT_FILE} does not exist.")
        print()
        print("Please create leads.csv in the project folder.")
        return

    # -----------------------------------------------------
    # Step 1 - Read leads
    # -----------------------------------------------------

    print()
    print("Step 1: Reading leads from CSV...")

    leads = read_leads()

    if not leads:

        print("No leads found.")
        return

    print(f"{len(leads)} leads loaded successfully.")

    # -----------------------------------------------------
    # Step 2 - Score leads
    # -----------------------------------------------------

    print()
    print("Step 2: Calculating lead scores...")

    scored_leads = score_leads(leads)

    print("Lead scoring completed successfully.")

    # -----------------------------------------------------
    # Step 3 - Display results
    # -----------------------------------------------------

    print()
    print("Step 3: Displaying lead results...")

    display_results(scored_leads)

    # -----------------------------------------------------
    # Step 4 - Display summary
    # -----------------------------------------------------

    print()
    print("Step 4: Generating lead summary...")

    display_summary(scored_leads)

    # -----------------------------------------------------
    # Step 5 - Display Hot Leads
    # -----------------------------------------------------

    print()
    print("Step 5: Finding Hot Leads...")

    display_hot_leads(scored_leads)

    # -----------------------------------------------------
    # Step 6 - Marketing source summary
    # -----------------------------------------------------

    print()
    print("Step 6: Analyzing marketing sources...")

    display_source_summary(scored_leads)

    # -----------------------------------------------------
    # Step 7 - Marketing actions
    # -----------------------------------------------------

    print()
    print("Step 7: Generating recommended marketing actions...")

    display_marketing_actions(scored_leads)

    # -----------------------------------------------------
    # Step 8 - Save results
    # -----------------------------------------------------

    print()
    print("Step 8: Saving final results...")

    save_results(scored_leads)

    # -----------------------------------------------------
    # Finished
    # -----------------------------------------------------

    print()
    print("=" * 90)
    print("                    PROCESS COMPLETED")
    print("=" * 90)

    print()
    print("Your lead scoring automation is complete.")
    print()
    print("Input file  :", INPUT_FILE)
    print("Output file :", OUTPUT_FILE)
    print()


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":
    main()