---
name: seo-wordpress
description: |
  WordPress SEO specialist skill for the Travel Insurance Center-Kenya plugin.
  Use when asked to improve SEO, add meta tags, schema markup, Open Graph, structured data,
  sitemap integration, keyword optimisation, canonical URLs, or page speed for the plugin's
  frontend pages and templates. Covers both on-page technical SEO (PHP/HTML output) and
  content-level recommendations.
  Trigger words: "SEO", "meta tags", "schema", "structured data", "Open Graph", "sitemap",
  "canonical", "page speed", "rich snippets", "search ranking", "keyword", "seo skill".
version: "1.0"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep"]
applyTo: "**/*.php, **/*.html, **/*.js, **/*.css"
---

# SEO Skill — Travel Insurance Center-Kenya (WordPress)

## Context

This skill targets a WordPress plugin that renders insurance policy pages, quote wizards, and
agency dashboards on the frontend. SEO improvements focus on:

- Technical on-page SEO output from PHP templates
- Structured data / JSON-LD for insurance products
- Social sharing (Open Graph, Twitter Cards)
- Core Web Vitals & page speed
- Keyword targeting for Kenyan travel insurance searches
- WordPress-specific integration (Yoast/RankMath compatibility)

---

## Execution Workflow

1. **Audit** — Identify the page/template/shortcode the user is targeting.
2. **Classify intent** — Which SEO domain applies? (See table below)
3. **Implement** — Apply changes directly to the relevant PHP/HTML files.
4. **Validate** — Check output renders valid HTML and no PHP errors.
5. **Document** — Note any new options/constants added to `key_facts.md`.

---

## Intent → Action Map

| User Request | Action |
|---|---|
| "Add meta tags" | Inject `<meta>` via `wp_head` hook in the relevant class |
| "Add schema / structured data" | Output JSON-LD `<script>` block via `wp_head` or inline |
| "Open Graph / social sharing" | Add `og:*` and `twitter:*` meta tags |
| "Add canonical URL" | Output `<link rel="canonical">` via `wp_head` |
| "Sitemap" | Register CPT/pages with WordPress sitemap or Yoast |
| "Page speed / Core Web Vitals" | Audit asset loading, defer JS, lazy-load images |
| "Keyword optimisation" | Review heading hierarchy, title tags, content density |
| "Rich snippets / FAQ schema" | Add `FAQPage` or `Product` JSON-LD |

---

## WordPress SEO Implementation Patterns

### 1. Adding Meta Tags via `wp_head`

Hook into `wp_head` inside the relevant class constructor. Always escape output.

```php
add_action( 'wp_head', [ $this, 'output_seo_meta' ] );

public function output_seo_meta(): void {
    if ( ! is_singular( 'policy' ) ) {
        return;
    }
    $post  = get_queried_object();
    $title = esc_attr( get_the_title( $post ) );
    $desc  = esc_attr( wp_strip_all_tags( get_the_excerpt( $post ) ) );
    $url   = esc_url( get_permalink( $post ) );
    $img   = esc_url( get_the_post_thumbnail_url( $post, 'large' ) );
    ?>
    <meta name="description" content="<?php echo $desc; ?>">
    <meta property="og:title" content="<?php echo $title; ?>">
    <meta property="og:description" content="<?php echo $desc; ?>">
    <meta property="og:url" content="<?php echo $url; ?>">
    <meta property="og:type" content="product">
    <?php if ( $img ) : ?>
        <meta property="og:image" content="<?php echo $img; ?>">
    <?php endif; ?>
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="<?php echo $url; ?>">
    <?php
}
```

### 2. JSON-LD Structured Data — Insurance Product

Use `InsuranceProduct` mapped to the closest Schema.org type (`Product` + `FinancialProduct`).

```php
public function output_schema_jsonld(): void {
    if ( ! is_singular( 'policy' ) ) {
        return;
    }
    $post      = get_queried_object();
    $name      = get_the_title( $post );
    $desc      = wp_strip_all_tags( get_the_excerpt( $post ) );
    $url       = get_permalink( $post );
    $logo_url  = get_option( 'maljani_company_logo_url', '' );

    $schema = [
        '@context'    => 'https://schema.org',
        '@type'       => 'Product',
        'name'        => $name,
        'description' => $desc,
        'url'         => $url,
        'brand'       => [
            '@type' => 'Organization',
            'name'  => 'Travel Insurance Center-Kenya',
            'url'   => home_url(),
        ],
    ];

    if ( $logo_url ) {
        $schema['brand']['logo'] = $logo_url;
    }

    echo '<script type="application/ld+json">'
        . wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
        . '</script>' . "\n";
}
```

### 3. Organization / LocalBusiness Schema (Site-wide)

Add once on all pages to establish the brand entity in Google's Knowledge Graph.

```php
$org_schema = [
    '@context'        => 'https://schema.org',
    '@type'           => 'InsuranceAgency',
    'name'            => 'Travel Insurance Center-Kenya',
    'url'             => home_url(),
    'areaServed'      => 'KE',
    'currenciesAccepted' => 'KES',
    'address'         => [
        '@type'           => 'PostalAddress',
        'addressCountry'  => 'KE',
    ],
];
```

### 4. FAQ Schema

For policy detail pages that include an FAQ section:

```php
$faq_schema = [
    '@context'   => 'https://schema.org',
    '@type'      => 'FAQPage',
    'mainEntity' => [
        [
            '@type'          => 'Question',
            'name'           => 'What does this travel insurance cover?',
            'acceptedAnswer' => [
                '@type' => 'Answer',
                'text'  => esc_html( get_post_meta( $post->ID, '_policy_coverage_summary', true ) ),
            ],
        ],
    ],
];
```

### 5. Yoast / RankMath Compatibility

Before outputting custom meta, check if a premium SEO plugin is active to avoid duplication:

```php
private function seo_plugin_active(): bool {
    return defined( 'WPSEO_VERSION' ) || defined( 'RANK_MATH_VERSION' );
}

public function output_seo_meta(): void {
    if ( $this->seo_plugin_active() ) {
        return; // Let Yoast/RankMath handle it
    }
    // ... custom output
}
```

### 6. Title Tag Customisation

```php
add_filter( 'document_title_parts', [ $this, 'filter_policy_title' ] );

public function filter_policy_title( array $title ): array {
    if ( is_singular( 'policy' ) ) {
        $title['tagline'] = 'Travel Insurance Center-Kenya';
    }
    return $title;
}
```

### 7. Page Speed — Asset Optimisation

```php
// Defer non-critical scripts
add_filter( 'script_loader_tag', function( $tag, $handle ) {
    $defer = [ 'maljani-client-dashboard', 'maljani-sales-page' ];
    if ( in_array( $handle, $defer, true ) ) {
        return str_replace( ' src=', ' defer src=', $tag );
    }
    return $tag;
}, 10, 2 );

// Lazy-load images in policy listings
add_filter( 'wp_get_attachment_image_attributes', function( $attr ) {
    $attr['loading'] = 'lazy';
    return $attr;
} );
```

---

## Target Keywords (Kenya Travel Insurance)

Primary cluster to use in title tags, headings, and content:

- Travel insurance Kenya
- Travel insurance Nairobi
- Travel insurance quotes Kenya
- Cheap travel insurance Kenya
- Medical travel insurance Kenya
- Annual multi-trip insurance Kenya
- Schengen visa travel insurance Kenya

Long-tail opportunities:
- Best travel insurance for Kenyan passport holders
- Travel insurance that covers COVID Kenya
- Single trip travel insurance Kenya

---

## SEO Checklist for New Pages/Shortcodes

When adding a new frontend-rendered page:

- [ ] Unique `<title>` tag via `document_title_parts` filter
- [ ] `<meta name="description">` (max 160 chars)
- [ ] `<link rel="canonical">` pointing to the canonical URL
- [ ] Open Graph `og:title`, `og:description`, `og:image`, `og:url`
- [ ] JSON-LD structured data block (`Product`, `FAQPage`, or `Organization`)
- [ ] Heading hierarchy: one `<h1>` per page, logical `<h2>`/`<h3>` nesting
- [ ] Image `alt` attributes on all `<img>` tags
- [ ] No duplicate content — use canonical or noindex for paginated/filtered URLs
- [ ] Check Yoast/RankMath is not outputting conflicting tags

---

## Security Rules

- Always use `esc_attr()`, `esc_url()`, `esc_html()`, `wp_strip_all_tags()` before SEO output.
- Never trust raw `$_GET`/`$_POST` in meta output — sanitize first.
- Use `wp_json_encode()` for JSON-LD, never `json_encode()` directly.
- Hook into `wp_head` with a priority > 10 to run after theme head, < 99 to run before closing `</head>`.
