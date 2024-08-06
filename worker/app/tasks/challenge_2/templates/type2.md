# {{ report_name }}

**Creation Date**: {{ creation_date }}

| ID  | Department | Hired |
|-----|--------------|-------|
{% for row in data %}| {{ row.id }} | {{ row.department }} | {{ row.hired }} |
{% endfor %}
