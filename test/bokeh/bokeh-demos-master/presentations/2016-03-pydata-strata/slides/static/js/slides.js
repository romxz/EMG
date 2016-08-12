function isPreview() {
  return !!window.location.search.match(/preview/gi);
}

function initializeReveal() {
  // Full list of configuration options available at:
  // https://github.com/hakimel/reveal.js#configuration
  Reveal.initialize({
    controls: true,
    progress: true,
    history: true,
    center: true,
    transition: 'slide', // none/fade/slide/convex/concave/zoom
    transitionSpeed: isPreview() ? 'fast' : 'default',
    embedded: isPreview() ? true : false,
    width: 1280,
    height: 720,

      // Optional reveal.js plugins
    dependencies: [
    { src: 'revealjs/lib/js/classList.js', condition: function() { return !document.body.classList; } },
    { src: 'revealjs/plugin/markdown/marked.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
    { src: 'revealjs/plugin/markdown/markdown.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); }, callback: function() { externalLinksInNewWindow(); } },
      { src: 'revealjs/plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } },
      { src: 'revealjs/plugin/zoom-js/zoom.js', async: true },
        { src: 'revealjs/plugin/notes/notes.js', async: true }
    ]
  });
}

function highlightAnyCodeBlocks() {
  $(document).ready(function() {
    $('pre code').each(function(i, block) {
      hljs.highlightBlock(block);
    });
  });
}

function insertMarkdownReference() {
  var markdownReference = $('<section/>', {
    'data-markdown': "../slides.md",
    'data-separator': "^-( *)-( *)-( *-*)*",
    'data-separator-notes': "^Note:",
    'data-charset': "utf-8"
  });

  $('.slides').html(markdownReference);
}

function scrollToCurrentSlide() {
  var i = Reveal.getIndices();
  Reveal.slide(i.h, i.v, i.f);
}

function reloadMarkdown() {
  insertMarkdownReference();
  RevealMarkdown.initialize();
  highlightAnyCodeBlocks();
  scrollToCurrentSlide();
}

function externalLinksInNewWindow() {
  $(document.links).filter(function() {
    return this.hostname != window.location.hostname;
  }).attr('target', '_blank');
}

insertMarkdownReference();
initializeReveal();

// Monkey patch Reveal so we can reload markdown through an
// inter window message (using the reveal rpc api)
// (yes, reveal has an rpc api!)
// see save.js
Reveal.reloadMarkdown = reloadMarkdown;
