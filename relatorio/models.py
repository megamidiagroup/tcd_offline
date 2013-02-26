# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import models
from django.contrib.auth.models import User as UserAdmin
from django.db.models import Q

from mega.models import Rede

# Create your models here.

### Tabela para os relatorios de pontos e avaliações
class AlunoCadastrado(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Relatório.')
    user     = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    count    = models.IntegerField(default=0, verbose_name='Contagem de exportações')
    acesso   = models.IntegerField(default=0, verbose_name='Contagem de acessos')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.rede

    def set_extrato(self, p):

        ac = AlunoCadastrado.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if ac.count() > 0:
            ac = ac[0]
        else:
            ac = AlunoCadastrado()
            ac.rede = p['rede']
            ac.user = p['user']

        ac.count += 1

        return ac.save()

    def set_acesso(self, p):

        ac = AlunoCadastrado.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if ac.count() > 0:
            ac = ac[0]
        else:
            ac = AlunoCadastrado()
            ac.rede = p['rede']
            ac.user = p['user']

        ac.acesso += 1

        return ac.save()

    class Meta:
        verbose_name        = u'Aluno Cadastrado'
        verbose_name_plural = u'Alunos Cadastrados'
        ordering            = ['-date']


### Tabela para os relatorios de certificados dos alunos por filial
class AlunoCertificado(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Relatório.')
    user     = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    count    = models.IntegerField(default=0, verbose_name='Contagem de exportações')
    acesso   = models.IntegerField(default=0, verbose_name='Contagem de acessos')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.rede

    def set_extrato(self, p):

        ac = AlunoCertificado.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if ac.count() > 0:
            ac = ac[0]
        else:
            ac = AlunoCertificado()
            ac.rede = p['rede']
            ac.user = p['user']

        ac.count += 1

        return ac.save()

    def set_acesso(self, p):

        ac = AlunoCertificado.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if ac.count() > 0:
            ac = ac[0]
        else:
            ac = AlunoCertificado()
            ac.rede = p['rede']
            ac.user = p['user']

        ac.acesso += 1

        return ac.save()

    class Meta:
        verbose_name        = u'Aluno Certificado'
        verbose_name_plural = u'Alunos Certificados'
        ordering            = ['-date']
        
        
### Tabela para os relatorios de quantidade de treinamentos concluídos do aluno
class TreinamentoConcluido(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Relatório.')
    user     = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    count    = models.IntegerField(default=0, verbose_name='Contagem de exportações')
    acesso   = models.IntegerField(default=0, verbose_name='Contagem de acessos')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.rede

    def set_extrato(self, p):

        tc = TreinamentoConcluido.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if tc.count() > 0:
            tc = tc[0]
        else:
            tc = TreinamentoConcluido()
            tc.rede = p['rede']
            tc.user = p['user']

        tc.count += 1

        return tc.save()

    def set_acesso(self, p):

        tc = TreinamentoConcluido.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if tc.count() > 0:
            tc = tc[0]
        else:
            tc = TreinamentoConcluido()
            tc.rede = p['rede']
            tc.user = p['user']

        tc.acesso += 1

        return tc.save()

    class Meta:
        verbose_name        = u'Treinamento concluído do aluno'
        verbose_name_plural = u'Treinamentos concluídos do aluno'
        ordering            = ['-date']
        
        
### Tabela para os relatorios de pontuação listado por alunos
class PontuacaoAluno(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Relatório.')
    user     = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    count    = models.IntegerField(default=0, verbose_name='Contagem de exportações')
    acesso   = models.IntegerField(default=0, verbose_name='Contagem de acessos')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.rede

    def set_extrato(self, p):

        pa = PontuacaoAluno.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if pa.count() > 0:
            pa = pa[0]
        else:
            pa = PontuacaoAluno()
            pa.rede = p['rede']
            pa.user = p['user']

        pa.count += 1

        return pa.save()

    def set_acesso(self, p):

        pa = PontuacaoAluno.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if pa.count() > 0:
            pa = pa[0]
        else:
            pa = PontuacaoAluno()
            pa.rede = p['rede']
            pa.user = p['user']

        pa.acesso += 1

        return pa.save()

    class Meta:
        verbose_name        = u'Pontuação do Aluno'
        verbose_name_plural = u'Pontuação dos Alunos'
        ordering            = ['-date']
        
        
### Tabela para os relatorios treinamentos cadastrados por rede ou filial
class TreinamentoCadastrado(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Relatório.')
    user     = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    count    = models.IntegerField(default=0, verbose_name='Contagem de exportações')
    acesso   = models.IntegerField(default=0, verbose_name='Contagem de acessos')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.rede

    def set_extrato(self, p):

        tc = TreinamentoCadastrado.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if tc.count() > 0:
            tc = tc[0]
        else:
            tc = TreinamentoCadastrado()
            tc.rede = p['rede']
            tc.user = p['user']

        tc.count += 1

        return tc.save()

    def set_acesso(self, p):

        tc = TreinamentoCadastrado.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if tc.count() > 0:
            tc = tc[0]
        else:
            tc = TreinamentoCadastrado()
            tc.rede = p['rede']
            tc.user = p['user']

        tc.acesso += 1

        return tc.save()

    class Meta:
        verbose_name        = u'Número de Treinamento e aluno Cadastrado'
        verbose_name_plural = u'Número de Treinamentos e alunos Cadastrados'
        ordering            = ['-date']
        
        
        
### Tabela para os relatorios e graficos
class RelatorioGrafico(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Relatório.')
    user     = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    count    = models.IntegerField(default=0, verbose_name='Contagem de exportações')
    acesso   = models.IntegerField(default=0, verbose_name='Contagem de acessos')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.rede

    def set_extrato(self, p):

        rg = RelatorioGrafico.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if rg.count() > 0:
            rg = rg[0]
        else:
            rg = RelatorioGrafico()
            rg.rede = p['rede']
            rg.user = p['user']

        rg.count += 1

        return rg.save()

    def set_acesso(self, p):

        rg = RelatorioGrafico.objects.filter( Q(rede = p['rede']), Q(user = p['user']) )

        if rg.count() > 0:
            rg = rg[0]
        else:
            rg = RelatorioGrafico()
            rg.rede = p['rede']
            rg.user = p['user']

        rg.acesso += 1

        return rg.save()

    class Meta:
        verbose_name        = u'Relatório / Gráfico'
        verbose_name_plural = u'Relatórios / Gráficos'
        ordering            = ['-date']