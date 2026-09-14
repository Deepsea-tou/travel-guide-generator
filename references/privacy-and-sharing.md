# Privacy and sharing gate

Personal outputs may contain private notes needed during planning. Share outputs are new sanitized bundles, never renamed copies of personal files.

Before share export, remove or generalize real names, private events, contact details, booking/order identifiers, account data, home and lodging addresses, local absolute paths, internal links, and unnecessary exact tracks. Remove local knowledge provenance and hidden fields. Images require a separate metadata/EXIF check before publication.

Apply sanitization before rendering every format. Remember that ICS exposes exact time/location, GeoJSON exposes coordinates, JSON preserves hidden fields, and HTML may contain comments or embedded data. If exact coordinates are not necessary for the audience, omit or coarsen them in the structured share input.

After export, scan HTML, Markdown, JSON, ICS, and GeoJSON for configured sensitive values, absolute-path patterns, file URLs, and raw private fields. A residual match blocks publication. The message used to deliver a file locally may contain a clickable local link, but that path must not appear inside the share artifact itself.
