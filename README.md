# POAM-Pilot

### [DOCUMENTATION](https://github.com/Elevated-Standards/POAM-Pilot/wiki)

The POAM (Plan of Action and Milestones) Pilot App is a web-based application designed to streamline the tracking, management, and reporting of security vulnerabilities and compliance requirements. The app integrates with popular vulnerability scanning tools (e.g., AWS Inspector, Tenable) and provides an efficient way to manage POA&M items for compliance frameworks such as FedRAMP.

### Key Features

1. **Integration with Scanning Tools**:
   - Fetch vulnerability findings from AWS Inspector and Tenable.
   - Support configuration scan findings and general vulnerability scan findings.

2. **POA&M Management**:
   - Automatically map findings to a FedRAMP POA&M template.
   - Categorize and manage findings as **Open POA&M Items**, **Closed POA&M Items**, or **Configuration Findings**.
   - Track additional details such as asset identifiers, remediation plans, risk adjustments, and vendor dependencies.

3. **Asset Management**:
   - Link findings to specific assets (e.g., servers, applications) to provide context for vulnerabilities.
   - Maintain an inventory of assets with detailed information such as owner, type, and descriptions.

4. **Excel Reporting**:
   - Export POA&M data into a FedRAMP-compliant Excel template with predefined tabs for Open POA&M Items, Closed POA&M Items, and Configuration Findings.
   - Preserve formatting, milestones, and compliance-specific fields during export.

5. **Integration Management**:
   - Configure integrations with AWS Inspector, Tenable, GitHub (for issue creation), and Google Spaces (for notifications).
   - Provide seamless data fetching and updates from connected systems.

6. **Dashboard and Reporting**:
   - Centralized dashboard for quick insights into the status of POA&M items and scan results.
   - Paginated scan results with filtering capabilities for better visibility into vulnerabilities.

7. **Compliance Tracking**:
   - Include tracking fields such as "Binding Operational Directive 22-01," "False Positives," "Operational Requirements," and CVE details.
   - Provide compliance insights with supporting documentation fields and comments.

8. **Dockerized Deployment**:
   - Easily deployable using Docker and Docker Compose.
   - Includes a lightweight, production-ready Flask backend.

---

### How It Works

1. **Scanning and Integration**:
   - The app fetches findings from connected tools (e.g., AWS Inspector, Tenable).
   - Findings are categorized and mapped to POA&M items.

2. **POA&M Tracking**:
   - Users can view, update, and link findings to assets.
   - The app keeps track of milestones, risk ratings, remediation plans, and completion dates.

3. **Exporting and Reporting**:
   - Users can export POA&M data into a predefined Excel template for compliance reporting.
   - The export includes all relevant details for Open, Closed, and Configuration Findings.


---

### Use Cases

1. **Compliance Teams**:
   - Automate the generation and tracking of POA&M items for frameworks like FedRAMP.
2. **Security Teams**:
   - Manage and prioritize vulnerabilities from various scanning tools in a centralized system.
3. **IT Managers**:
   - Gain visibility into open issues, remediation plans, and asset dependencies.
