import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import logging 
logging.basicConfig(level=logging.INFO)
logging.info(">>>>>>>> ")
# Load CSV data
csv_file = "/Users/Admin/Documents/donorgiftscript/anoncopy.csv"  # Update this with the correct file path
df = pd.read_csv(csv_file)

# Ensure output directory exists
output_dir = "/Users/Admin/Documents/donorgiftscript/donation_summaries"
os.makedirs(output_dir, exist_ok=True)

# Get unique donor IDs
unique_donors = df["REID"].unique()
logging.info(">>>>>>>> " + unique_donors )
# Loop over each donor and generate a PDF
for donor_id in unique_donors:
    # Filter donations for this donor
    filtered_df = df[df["REID"] == donor_id]
    donor_name = filtered_df["Name"].unique()[0]
    logging.info(donor_name)

    # Generate a PDF filename based on the donor ID
    pdf_filename = os.path.join(output_dir, f"donation_summary_{donor_name}.pdf")

    # Create the PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # PDF Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Action Against Hunger - Donation Summary")

    # Donor Information
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Donor ID: {donor_id}")

    # Table Headers
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 120, "Date")
    c.drawString(200, height - 120, "Amount")

    # Insert Data
    y_position = height - 140
    c.setFont("Helvetica", 12)
    
    for _, row in filtered_df.iterrows():
        
        c.drawString(50, y_position, str(row["Gift Date"]))
        c.drawString(200, y_position, str(row["Gift Amount"]))
        y_position -= 20  # Move down for next row

        # Page break if needed
        if y_position < 50:
            c.showPage()  # New page
            y_position = height - 50  # Reset position

    # Save PDF
    c.save()
    print(f"PDF generated: {pdf_filename}")

print("Batch PDF generation complete!")
