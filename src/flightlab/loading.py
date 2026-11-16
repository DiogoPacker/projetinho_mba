"""Tela de espera da aplicação: animação CSS local, sem dependências externas."""

LOADING_HTML = """
<style>
.flightlab-loading {
    padding: 2rem; margin: 1rem 0 1.5rem;
    border: 1px solid #2563eb55; border-radius: 20px;
    background: linear-gradient(135deg, #162236, #0b1220);
    color: #f1f5f9; text-align: center;
}
.flightlab-loading .flight-path {
    position: relative; max-width: 320px; height: 52px; margin: 0 auto 1rem;
    overflow: hidden;
}
.flightlab-loading .flight-path::before {
    content: ''; position: absolute; top: 30px; left: 8%; right: 8%;
    border-top: 2px dashed #60a5fa66;
}
.flightlab-loading .plane {
    position: absolute; font-size: 2rem; left: 0; top: 0;
    animation: flightlab-fly 2.8s ease-in-out infinite;
}
.flightlab-loading h3 { color: #f1f5f9; margin: 0 0 .5rem; }
.flightlab-loading p { color: #cbd5e1; margin: 0 auto 1rem; max-width: 520px; }
.flightlab-loading .track {
    max-width: 280px; height: 4px; margin: 1rem auto 0;
    background: #334155; border-radius: 4px; overflow: hidden;
}
.flightlab-loading .track::after {
    content: ''; display: block; width: 40%; height: 100%;
    border-radius: 4px; background: #60a5fa;
    animation: flightlab-progress 1.8s ease-in-out infinite;
}
@keyframes flightlab-fly {
    0% { left: 0; opacity: 0; transform: translateY(8px); }
    15%, 80% { opacity: 1; }
    100% { left: 85%; opacity: 0; transform: translateY(-8px); }
}
@keyframes flightlab-progress {
    from { transform: translateX(-110%); }
    to { transform: translateX(360%); }
}
@media (prefers-reduced-motion: reduce) {
    .flightlab-loading .plane { animation: none; left: 45%; }
    .flightlab-loading .track::after { animation: none; width: 100%; }
}
</style>
<section class="flightlab-loading" role="status" aria-live="polite" aria-atomic="true">
    <div class="flight-path" aria-hidden="true"><span class="plane">✈</span></div>
    <h3>Preparando sua análise</h3>
    <p>Aguarde um instante. Estamos carregando os dados de voos,
    o modelo e os indicadores do dashboard.</p>
    <div class="track" aria-hidden="true"></div>
</section>
"""
