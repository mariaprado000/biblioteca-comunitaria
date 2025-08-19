"""
Context processors para disponibilizar informações globais nos templates
"""

def user_groups(request):
    """
    Adiciona informações sobre grupos do usuário aos templates
    """
    context = {
        'user_is_funcionario': False,
        'user_is_leitor': False,
    }
    
    if request.user.is_authenticated:
        user_groups = request.user.groups.values_list('name', flat=True)
        context.update({
            'user_is_funcionario': 'Funcionarios' in user_groups,
            'user_is_leitor': 'Leitores' in user_groups,
            'user_groups': list(user_groups),
        })
    
    return context