# Schema inventory - August 16, 2026

## Before normalization

The site used a mixture of Article and NewsMediaOrganization records. Several older article templates omitted one or more of: organizational author, image, article section, publisher logo, or breadcrumb markup. Social metadata referenced an SVG card, which is not reliably rendered by major sharing surfaces.

## Normalization applied

- Replaced legacy SVG social-card references on 0 non-India HTML pages with `/assets/social-card.png`.
- Standardized Article / NewsArticle fields on 56 records: organizational author, raster image, article section, publisher identity and publisher logo.
- Added BreadcrumbList records to 1 content articles.
- Added Dataset records to 0 data pages that expose a CSV download.

## Deliberate exclusions

India pages were not altered. Organization contactPoint and legal identity were not added because no verified public contact address or operating entity exists in the source repository.
