// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded "><a href="index.html"><strong aria-hidden="true">1.</strong> Introduction / Case Studies</a></li><li class="chapter-item expanded "><a href="transition-guide.html"><strong aria-hidden="true">2.</strong> Transitioning workloads to AWS Graviton</a></li><li class="chapter-item expanded "><a href="optimizing.html"><strong aria-hidden="true">3.</strong> Optimizing for Graviton</a></li><li><ol class="section"><li class="chapter-item expanded "><a href="c-c++.html"><strong aria-hidden="true">3.1.</strong> C/C++</a></li><li class="chapter-item expanded "><a href="golang.html"><strong aria-hidden="true">3.2.</strong> Go</a></li><li class="chapter-item expanded "><a href="java.html"><strong aria-hidden="true">3.3.</strong> Java</a></li><li class="chapter-item expanded "><a href="CommonNativeJarsTable.html"><strong aria-hidden="true">3.4.</strong> JAR files</a></li><li class="chapter-item expanded "><a href="dotnet.html"><strong aria-hidden="true">3.5.</strong> .NET</a></li><li class="chapter-item expanded "><a href="nodejs.html"><strong aria-hidden="true">3.6.</strong> Node.JS</a></li><li class="chapter-item expanded "><a href="php.html"><strong aria-hidden="true">3.7.</strong> PHP</a></li><li class="chapter-item expanded "><a href="php-opcache-al2.html"><strong aria-hidden="true">3.8.</strong> PHP OPcache</a></li><li class="chapter-item expanded "><a href="python.html"><strong aria-hidden="true">3.9.</strong> Python</a></li><li class="chapter-item expanded "><a href="rust.html"><strong aria-hidden="true">3.10.</strong> Rust</a></li><li class="chapter-item expanded "><a href="R.html"><strong aria-hidden="true">3.11.</strong> R</a></li><li class="chapter-item expanded "><a href="DataAnalytics.html"><strong aria-hidden="true">3.12.</strong> Spark</a></li><li class="chapter-item expanded "><a href="aws-lambda/index.html"><strong aria-hidden="true">3.13.</strong> AWS Lambda</a></li></ol></li><li class="chapter-item expanded "><a href="os.html"><strong aria-hidden="true">4.</strong> Operating Systems support</a></li><li class="chapter-item expanded "><a href="containers.html"><strong aria-hidden="true">5.</strong> Containers on Graviton</a></li><li class="chapter-item expanded "><a href="software/ChromeAndPuppeteer.html"><strong aria-hidden="true">6.</strong> Headless website testing with Chrome and Puppeteer</a></li><li class="chapter-item expanded "><a href="software/librdkafka.html"><strong aria-hidden="true">7.</strong> Kafka</a></li><li class="chapter-item expanded "><a href="amis_cf_sm.html"><strong aria-hidden="true">8.</strong> AMIs for Graviton</a></li><li class="chapter-item expanded "><a href="managed_services.html"><strong aria-hidden="true">9.</strong> AWS Managed Services available on Graviton</a></li><li class="chapter-item expanded "><a href="isv.html"><strong aria-hidden="true">10.</strong> Third-party Software Vendors</a></li><li class="chapter-item expanded "><a href="HPC/index.html"><strong aria-hidden="true">11.</strong> HPC (High Perf Computing)</a></li><li class="chapter-item expanded "><a href="HPC/setup-an-ec2-hpc-instance.html"><strong aria-hidden="true">12.</strong> Build HPC software</a></li><li class="chapter-item expanded affix "><li class="part-title">Machine Learning</li><li class="chapter-item expanded "><a href="machinelearning/pytorch.html"><strong aria-hidden="true">13.</strong> PyTorch</a></li><li class="chapter-item expanded "><a href="machinelearning/tensorflow.html"><strong aria-hidden="true">14.</strong> TensorFlow</a></li><li class="chapter-item expanded "><a href="machinelearning/llama.cpp.html"><strong aria-hidden="true">15.</strong> llama.cpp</a></li><li class="chapter-item expanded "><a href="machinelearning/vllm.html"><strong aria-hidden="true">16.</strong> vLLM</a></li><li class="chapter-item expanded "><a href="machinelearning/onnx.html"><strong aria-hidden="true">17.</strong> ONNX</a></li><li class="chapter-item expanded affix "><li class="part-title">Performance Runbook</li><li class="chapter-item expanded "><a href="perfrunbook/index.html"><strong aria-hidden="true">18.</strong> Pre-requisites and FAQ </a></li><li class="chapter-item expanded "><a href="perfrunbook/intro_to_benchmarking.html"><strong aria-hidden="true">19.</strong> Introduction to Benchmarking</a></li><li class="chapter-item expanded "><a href="perfrunbook/system-load-and-compute-headroom.html"><strong aria-hidden="true">20.</strong> System Load and Compute Headroom</a></li><li class="chapter-item expanded "><a href="perfrunbook/defining_your_benchmark.html"><strong aria-hidden="true">21.</strong> Defining your benchmark</a></li><li class="chapter-item expanded "><a href="perfrunbook/configuring_your_loadgen.html"><strong aria-hidden="true">22.</strong> Configuring your load generator</a></li><li class="chapter-item expanded "><a href="perfrunbook/configuring_your_sut.html"><strong aria-hidden="true">23.</strong> Configuring your system-under-test environment</a></li><li class="chapter-item expanded "><a href="perfrunbook/debug_system_perf.html"><strong aria-hidden="true">24.</strong> Debugging performance — “What part of the system is slow?”</a></li><li class="chapter-item expanded "><a href="perfrunbook/debug_code_perf.html"><strong aria-hidden="true">25.</strong> Debugging performance — “What part of the code is slow?”</a></li><li class="chapter-item expanded "><a href="perfrunbook/debug_hw_perf.html"><strong aria-hidden="true">26.</strong> Debugging performance — “What part of the hardware is slow?”</a></li><li class="chapter-item expanded "><a href="perfrunbook/optimization_recommendation.html"><strong aria-hidden="true">27.</strong> Optimizing performance</a></li><li class="chapter-item expanded "><a href="perfrunbook/appendix.html"><strong aria-hidden="true">28.</strong> Appendix — Additional resources</a></li><li class="chapter-item expanded "><a href="perfrunbook/references.html"><strong aria-hidden="true">29.</strong> References</a></li><li class="chapter-item expanded affix "><li class="part-title">Deep dive</li><li class="chapter-item expanded "><a href="runtime-feature-detection.html"><strong aria-hidden="true">30.</strong> Runtime feature detection</a></li><li class="chapter-item expanded "><a href="dpdk_spdk.html"><strong aria-hidden="true">31.</strong> DPDK, SPDK, and other datapath software</a></li><li class="chapter-item expanded "><a href="SIMD_and_vectorization.html"><strong aria-hidden="true">32.</strong> Taking advantage of Arm Advanced SIMD instructions</a></li><li class="chapter-item expanded "><a href="arm64-assembly-optimization.html"><strong aria-hidden="true">33.</strong> Assembly Optimization Guide for Graviton Arm64 Processors</a></li><li class="chapter-item expanded "><a href="Monitoring_Tools_on_Graviton.html"><strong aria-hidden="true">34.</strong> Profiling</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded affix "><a href="howtoresources.html">How To Resources</a></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split("#")[0].split("?")[0];
        if (current_page.endsWith("/")) {
            current_page += "index.html";
        }
        var links = Array.prototype.slice.call(this.querySelectorAll("a"));
        var l = links.length;
        for (var i = 0; i < l; ++i) {
            var link = links[i];
            var href = link.getAttribute("href");
            if (href && !href.startsWith("#") && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The "index" page is supposed to alias the first chapter in the book.
            if (link.href === current_page || (i === 0 && path_to_root === "" && current_page.endsWith("/index.html"))) {
                link.classList.add("active");
                var parent = link.parentElement;
                if (parent && parent.classList.contains("chapter-item")) {
                    parent.classList.add("expanded");
                }
                while (parent) {
                    if (parent.tagName === "LI" && parent.previousElementSibling) {
                        if (parent.previousElementSibling.classList.contains("chapter-item")) {
                            parent.previousElementSibling.classList.add("expanded");
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        var sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via "next/previous chapter" buttons
            var activeSection = document.querySelector('#sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        var sidebarAnchorToggles = document.querySelectorAll('#sidebar a.toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(function (el) {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define("mdbook-sidebar-scrollbox", MDBookSidebarScrollbox);
