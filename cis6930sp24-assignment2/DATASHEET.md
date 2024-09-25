## Datasheet for Norman Police Department Augmented Daily Incident Report Dataset

## Creators
The "Norman Police Department Augmented Daily Incident Report Dataset" was generated programmatically as part of a course project aimed at applying data science techniques to real-world public safety data by augmenting incident report from Norman Police department. The program used for dataset generation, along with the dataset itself, can be accessed on GitHub [here](https://github.com/nischithbo/cis6930sp24-assignment2).

## Purpose
The primary purpose of this dataset is to enrich the raw, daily incident reports collected by the Norman Police Department with additional context, insights, and synthesized attributes to facilitate more comprehensive analysis. By augmenting the data, we aim to offer researchers, policy makers, and public safety officials a deeper understanding of incident patterns, response efficacy, and potential areas for intervention.

## Motivation

**What specific objectives guided the augmentation of this dataset?**

The augmentation of the "Norman Police Department Augmented Daily Incident Report Dataset" was driven by the objective to provide a more granular and comprehensive understanding of public safety incidents. By incorporating additional features such as the time of day, weather conditions, and specific location data, the aim was to uncover patterns and correlations that raw data might not reveal. This enriched dataset allows for a multifaceted analysis of incidents, intending to improve predictive policing, enhance resource deployment strategies, and ultimately contribute to more effective public safety measures.

**How does this dataset contribute to understanding public safety, incident management, or social studies?**

The enriched dataset offers a valuable resource for a wide range of stakeholders interested in public safety, incident management, and social studies. By presenting incidents with added context—such as environmental conditions and temporal patterns—it facilitates a deeper analysis of crime and safety trends. This analysis can inform policy-making, community policing strategies, and social research, offering insights into how different factors contribute to safety and risk in the community. Furthermore, it serves as an educational tool, enabling students and researchers to explore the intersections of environment, society, and public policy through data.

## Data Collection Process

The data for the "Norman Police Department Augmented Daily Incident Report Dataset" was collected through an automated process that programmatically downloaded daily incident report PDFs from the Norman Police Department's website. This process utilized a Python-based PDF data extractor module to process each PDF, extracting data row by row for individual incidents. The data was then segmented into predefined columns corresponding to the dataset's fields. This automated extraction, followed by data further preprocessing, structured the raw data into a usable format. Further augmentation ensured the dataset's analytical value and reliability. This methodical approach guarantees a comprehensive and up-to-date dataset, ready for analysis and application in public safety, policy-making, and research.

## Scope


The dataset spans all reported incidents within the Norman Police Department's jurisdiction throughout the year. It is structured to provide a holistic view of public safety incidents, covering a wide array of incident types from traffic-related stops to more severe criminal activities. Geographic coverage extends to all areas under the Norman Police Department, ensuring a city-wide analysis of incident occurrences and patterns.

Temporal coverage is comprehensive, capturing incidents throughout the entire year, allowing for seasonal and time-of-day analyses. The data is enriched to support multifaceted analyses, including temporal trends, geographic distribution, incident severity, and the impact of environmental factors such as weather on public safety.

This dataset is designed with the granularity to support both broad trend analyses and detailed studies on specific types of incidents, making it a valuable resource for operational planning, policy development, and academic research in public safety and criminal justice.

## Methedology

**What specific data augmentation techniques were applied ?**

In the development of the "Norman Police Department Augmented Daily Incident Report Datase" several data augmentation techniques were meticulously applied to enrich the original dataset. These included the synthesis of new records to fill gaps where data might be missing or sparse, ensuring a more comprehensive dataset. Data interpolation methods were utilized to estimate and integrate values for environmental conditions like weather at the time of each incident, based on available meteorological data. Furthermore, natural language processing (NLP) techniques were employed to categorize and rank the nature of the incident and severity of incidents from narrative descriptions in police reports, providing structured, analyzable data points from unstructured text.

**How were fairness and bias addressed during the data augmentation process?**

During the data augmentation process for the "Norman Police Department Augmented Daily Incident Report Dataset," careful steps were taken to address fairness and bias, ensuring the dataset's integrity and usefulness. Since the Norman Police Department comprehensively reports incidents covering all locations, times, and days of the week throughout the year, the dataset inherently encompasses a wide range of incidents. This broad coverage helps mitigate biases related to geographic location, time-based occurrences, and day-specific activities. By compiling incidents uniformly across all months, the dataset avoids seasonal biases and presents an equitable view of incident occurrences throughout the year. This approach ensures that the dataset provides a balanced representation of incidents, contributing to more accurate and fair analyses and insights. Additionally, the ranking of location and nature were solely based on their frequency in the actual reports, which further ensures an objective measure for understanding incident patterns and supports equitable representation of different incident types and locations within the dataset.

## Data Quality and Limitations

**How is the quality of the augmented data ensured or verified?**

The quality of the augmented data in the "Norman Police Department Augmented Daily Incident Report Dataset" is meticulously ensured and verified through several robust measures, leveraging the inherent reliability of the source data and the integrity of augmentation processes. The Norman Police Department ensures that all incidents reported are verified, guaranteeing that only valid and confirmed reports contribute to the dataset. Throughout the augmentation phase, the dataset's fidelity is further upheld by exclusively employing trusted and authoritative sources for supplementary information. Weather conditions relevant to each incident are accurately retrieved from a historical weather API, recognized for its comprehensive and reliable meteorological data. Similarly, the geocoding of incident locations relies on the precision of Google's Geocode API, ensuring exact geographic details are captured. The day and hour of each incident are derived directly from the date reported in the incident, allowing for precise temporal analysis. This methodical approach to data augmentation, grounded in verified incidents and reputable data sources, ensures the augmented dataset's quality and reliability for comprehensive public safety analysis. 

**What are the known limitations and biases of this dataset?**

The "Norman Police Department Augmented Daily Incident Report DataseT" has inherent limitations and potential biases that users should consider. The dataset's accuracy and completeness heavily rely on the initial incident reports provided by the Norman Police Department. Inaccuracies in these primary data sources could directly impact the dataset's quality. Furthermore, biases may emerge from the data augmentation techniques, especially when assumptions are made during data synthesis or when using external data sources that have their inherent biases, such as inaccuracies in historical weather data.

The methodology for addressing missing information on the location and nature of incidents—by ranking such entries based on the overall frequency of empty fields—introduces a systematic approach to handle data gaps. However, this could also affect the dataset's interpretive accuracy, as it approximates the significance of missing details. Additionally, the reliance on geocode API for precise location data can sometimes lead to inaccuracies, particularly if the API fails to return coordinates for specific addresses. In such cases, the dataset defaults to using weather data for the town's center, potentially misrepresenting the actual environmental conditions of an incident's location. These limitations underscore the complexities involved in accurately capturing and representing the full spectrum of public safety incidents within Norman.

## Data Fields and Descriptions

The "Norman Police Department Augmented Daily Incident Report Dataset" includes a variety of fields derived from original incident reports, enhanced with additional data through the augmentation process. Below are the details of each field in augmented dataset:

**Day of the Week**: Derived from the incident date, indicating the day of the week to facilitate analysis of weekly trends and is a numeric value in the range 1-7. Where 1 corresponds to Sunday and 7 corresonds of Saturday.

**Time of Day**: Extracted from the incident time, useful for identifying patterns at different times of the day. The time of data is a numeric code from 0 to 23 describing the hour of the incident.

**Weather**: ugmented data indicating the weather code at the time of the incident, obtained from a historical weather API, providing context on environmental influences. 

**Location Rank**: Introduced during augmentation, it ranks incident locations based on frequency, facilitating spatial analysis by highlighting areas with higher incident rates for resource allocation and intervention prioritization. Instances of equal frequency are assigned the same rank, preserving ties and allowing for equitable categorization and prioritization of incidents in subsequent analyses and resource allocation efforts.

**Side of Town**: A new field calculated based on the incident's location relative to the town center, offering insights into geographical distribution patterns. The side of town is one of eight items {N, S, E, W, NW, NE, SW, SE}.

**Incident Rank**: Introduced during augmentation, it ranks the nature of incident based on frequency. Instances of equal frequency are assigned the same rank, preserving ties and allowing for equitable categorization and prioritization of incidents in subsequent analyses and resource allocation efforts.

**Nature**: A description of the incident type, categorized for consistency.

**EMSSTAT**: Indicates the urgency and type of emergency medical response, if applicable, reflecting the incident's impact on public health services. 

## Usage and Applications

The "Norman Police Department Augmented Daily Incident Report Dataset" holds significant potential for various applications in public safety, policy-making, and academic research. Some of the key implications include:

**Resource Allocation**: Law enforcement agencies can utilize the dataset to allocate resources effectively by identifying high-incidence areas and periods, optimizing patrol routes, and enhancing emergency response strategies.

**Crime Prevention**: Policymakers can leverage the dataset to develop targeted crime prevention initiatives by analyzing incident trends, understanding underlying factors contributing to criminal activities, and implementing proactive measures.

**Policy Development**: Public safety policies and regulations can be informed by insights gained from analyzing the dataset. This includes designing crime reduction strategies, improving community policing approaches, and implementing evidence-based interventions.

**Academic Research**: Researchers across disciplines such as criminology, sociology, geography, and data science can utilize the dataset to explore various aspects of public safety dynamics. This includes studying spatial and temporal patterns of crime, evaluating the effectiveness of law enforcement interventions, and conducting predictive modeling to forecast future incident trends.

## Case Studies or Examples

Several potential case studies or examples demonstrate the practical utility of the dataset:

**Hotspot Analysis**: Researchers can conduct hotspot analysis to identify areas with high incident density, allowing law enforcement agencies to deploy resources strategically and target crime prevention efforts effectively.

**Temporal Analysis**: Analyzing incident data over time can reveal temporal patterns, such as spikes in certain types of crimes during specific hours or days, aiding in the development of time-sensitive policing strategies.

**Weather Impact Study**: Studying the correlation between weather conditions and incident rates can provide insights into how environmental factors influence crime, informing policies for weather-related emergency response and community safety measures.

**Community Policing Initiatives**: Law enforcement agencies can use the dataset to evaluate the impact of community policing initiatives on incident rates, fostering collaboration between police departments and local communities to address public safety concerns effectively.

## Access and Distribution
Access to the program used to generate the "Norman Police Department Augmented Daily Incident Report Dataset" is available through a private GitHub repository. Individuals or organizations interested in accessing the program can request permission by contacting the repository owner or administrator. Upon receiving a request, the owner or administrator will review it to ensure that the requester has a legitimate need for access and understands any associated terms or restrictions. Once approved, users will be granted access to the repository, enabling them to download, use, and potentially modify the program for their own purposes and generate the dataset.

## Maintenance and Updates

The program used to generate the dataset not only allows for the inclusion of new incident records but also facilitates enhancements to the dataset, ensuring it stays updated with the latest information. Users can utilize the program to incorporate additional features, refine existing data fields, or improve data quality measures. This ensures that the dataset remains relevant and continues to meet evolving needs over time. For inquiries about dataset maintenance and updates, users can contact the repository owner or administrator through their GitHub account.

## Incorporation of Feedback

Feedback received will be verified and assessed for accuracy and relevance. Upon verification, necessary modifications will be made to both the program and dataset to address reported inaccuracies or incorporate suggested improvements. Future versions of the dataset will reflect these changes, ensuring its ongoing accuracy and utility.

