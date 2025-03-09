import sys
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
import logging
import re

# Ensure a CSV file is provided
if len(sys.argv) < 2:
    print("Error: No CSV file provided.")
    sys.exit(1)

csv_file = sys.argv[1]  # Get the uploaded file path from Node.js

# Load CSV
df = pd.read_csv(csv_file)
output_dir = "generated_pdfs"
os.makedirs(output_dir, exist_ok=True)


# Ensure output directory exists
# output_dir = "/Users/Admin/Documents/donorgiftscript/donation_summaries"
# os.makedirs(output_dir, exist_ok=True)

# # Load CSV data
# csv_file = "/Users/Admin/Documents/donorgiftscript/anoncopy.csv"  # Update with correct path
# df = pd.read_csv(csv_file)

# Generate PDFs
# for donor_id in df["REID"].unique():
#     filtered_df = df[df["REID"] == donor_id]
#     donor_name = str(filtered_df["Name"].unique()[0])
#     pdf_filename = os.path.join(output_dir, f"{donor_name}.pdf")

#     c = canvas.Canvas(pdf_filename, pagesize=letter)
#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(50, 750, f"Donation Summary for {donor_name}")

#     y = 730
#     for _, row in filtered_df.iterrows():
#         c.drawString(50, y, f"{row['Gift Date']} - ${row['Gift Amount']:.2f}")
#         y -= 20

#     c.save()
#     print(f"PDF generated: {pdf_filename}")


# Set up logging
logging.basicConfig(level=logging.INFO)
logging.info("Starting PDF Generation...")


logo_path = "../assets/AAH_logo.png"

 
# Get unique donor IDs
unique_donors = df["REID"].unique()
logging.info(f"Unique Donors Found: {list(unique_donors)}")

# Loop over each donor and generate a PDF
for donor_id in unique_donors:
    # Filter donations for this donor
    filtered_df = df[df["REID"] == donor_id]

    if filtered_df.empty:
        logging.warning(f"No donations found for donor ID {donor_id}")
        continue

    # Get donor name safely
    donor_name = str(filtered_df["Name"].unique()[0])  # Ensure name is a string
    safe_donor_name = re.sub(r'[^\w\s-]', '', donor_name).replace(" ", "_")  # Sanitize filename

    donor_address_line1 = str(filtered_df["Address 1"].unique()[0])
    donor_address_line2 = str(f"{filtered_df["City"].unique()[0]}, {filtered_df["State"].unique()[0]} {filtered_df["Zip"].unique()[0]}")
    # Generate a PDF filename
    pdf_filename = os.path.join(output_dir, f"donation_summary_{safe_donor_name}.pdf")

    # Create the PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    if os.path.exists(logo_path):
        c.drawImage(logo_path, width - 250, height - 115, width=155, height=95)

    # **Header - Organization Info**
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Action Against Hunger USA")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 65, "One Whitehall Street, 2nd Floor")
    c.drawString(50, height - 80, "New York, NY 10004")
    c.drawString(50, height - 95, "212.967.7800 x777")
    c.drawString(50, height - 110, "donorservices@actionagainsthunger.org")
    c.drawString(50, height - 125, "actionagainsthunger.org")

    # **Tax ID**
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, height - 150, "Action Against Hunger’s Tax ID: 13-3327220")

    # **Donor Information**
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 185, f"{donor_name}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 200, donor_address_line1)
    c.drawString(50, height - 215, donor_address_line2)

    height = height - 25


    
    
    # **Title: "2024 DONATION SUMMARY"**
    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, height - 230, "2024 DONATION SUMMARY")

    # **Table Headers**
    # c.setFont("Helvetica-Bold", 14)
    # c.drawString(100, height - 265, "Date")
    # c.drawString(200, height - 265, "Amount")
    # c.drawString(300, height - 265, "Date")
    # c.drawString(400, height - 265, "Amount")
    # # c.drawString(150, height - 250, "Transaction ID")
    
    # # Draw a line under headers
    # c.setStrokeColor(colors.black)
    # c.line(85, height - 275, 485, height - 275)

    # **Insert Donation Data**
    y_position = height - 265
    
    c.setFont("Helvetica", 14)

    total_donation = 0
    right_down = 0
    for _, row in filtered_df.iterrows():
        gift_date = str(row["Gift Date"]).strip()
        # transaction_id = str(row["Transaction ID"]).strip()  # Assuming 'Transaction ID' column exists
        gift_amount = row['Gift Amount']
        total_donation += int(float(row["Gift Amount"].replace('$', '').replace(' ', '').replace(',', '')))
        if right_down == 0:
            c.drawString(100, y_position, gift_date)
            c.drawString(215, y_position, gift_amount)
            c.line(75, y_position - 10, 495, y_position - 10)
            right_down = 1
            # c.drawString(150, y_position, transaction_id)
        
        elif right_down == 1:
            c.drawString(300, y_position, gift_date)
            c.drawString(415, y_position, gift_amount)
            right_down = 0
            y_position -= 30  # Move down for next row
        
        # Page break if needed
        if y_position < 50:
            c.showPage()
            y_position = height - 50
            right_down = 0
    
    c.line(185, height - 245, 185, y_position - 10)
    c.line(285, height - 245, 285, y_position - 10)
    c.line(385, height - 245, 385, y_position - 10)
    # **Total Donation Amount**
    c.setFont("Helvetica-Bold", 14)
    c.drawString(150, y_position - 35, "TOTAL DONATION:")
    c.drawString(300, y_position - 35, f"${total_donation:.2f}")

    c.setStrokeColor(colors.green)  # Set border color
    c.setLineWidth(2)  # Set border thickness
    c.roundRect(75,  y_position - 45, 420, (height - 245) - (y_position - 45), radius=25, stroke=1, fill=0)  

    # **Footer - Tax Disclaimer**
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, y_position - 70, "The above donor(s) received no goods or services in exchange for this contribution.")
    c.drawString(50, y_position - 85, "Action Against Hunger USA is a 501(c)(3) not-for-profit organization.")
    c.drawString(50, y_position - 100, "All contributions are tax deductible to the full extent of the law.")

    # Save PDF
    c.save()
    logging.info(f"PDF generated: {pdf_filename}")

logging.info("Batch PDF generation complete!")
