// Shared site JS moved from templates
(function(){
    function atualizarSaldoRestante(){
        const select = document.getElementById('categoria_id');
        if(!select) return;
        const opt = select.options[select.selectedIndex];
        if(!opt) return;
        const limite = parseFloat(opt.dataset.limite || '0');
        const gasto = parseFloat(opt.dataset.gasto || '0');
        const valorInput = document.getElementById('valor');
        const valor = valorInput ? parseFloat(valorInput.value || '0') : 0;
        const restante = limite - gasto - valor;

        // support both id formats used across templates
        const el = document.getElementById('saldo_restante') || document.getElementById('saldo-restante');
        const info = document.getElementById('info-saldo') || document.getElementById('info_saldo');
        if(el){
            // numeric localized string, using comma as decimal separator for pt-BR
            el.textContent = Number.isFinite(restante) ? restante.toLocaleString('pt-BR', {minimumFractionDigits:2, maximumFractionDigits:2}) : '-';
            el.className = restante < 0 ? 'text-danger' : 'text-success';
        }
        if(info){
            if(select.value){
                info.style.display = 'block';
            } else {
                info.style.display = 'none';
            }
        }
    }

    function bindUpdates(){
        const select = document.getElementById('categoria_id');
        const valor = document.getElementById('valor');
        if(select) select.addEventListener('change', atualizarSaldoRestante);
        if(valor) valor.addEventListener('input', atualizarSaldoRestante);
    }

    document.addEventListener('DOMContentLoaded', function(){
        bindUpdates();
        atualizarSaldoRestante();
    });

    // expose for templates that may call it directly
    window.atualizarSaldoRestante = atualizarSaldoRestante;
})();
