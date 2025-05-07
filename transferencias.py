import auxiliar
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import UnexpectedAlertPresentException


def iniciar_automacao(usuario, senha, cd, departamento_responsavel, area, nv1, nv2, motivo, cod_motivo):

    def fazer_login_people(usuario, senha):
        """" 
            Faz login no sistema PeopleSoft 
        """

        driver.maximize_window()
        driver.get('http://peoplesoft.dsp.int/psp/dpsperp_1/EMPLOYEE/ERP/c/MAINTAIN_INVENTORY.DSP_TRANS_LOC.GBL')
        driver.find_element(By.CSS_SELECTOR, 'input#userid').send_keys(usuario)
        driver.find_element(By.CSS_SELECTOR, 'input#pwd').send_keys(senha)
        driver.find_element(By.CSS_SELECTOR, 'input[name="Submit"]').click()

    def preencher_cabecalho(cd, departamento_responsavel):
        """"
            Preenche o cabeçalho da página.
            VD e também setor responsável.
        """
        driver.find_element(By.CSS_SELECTOR, 'a[name="tab1"]').click()
        esperar_carregamento_pagina()
        while True:
            try:
                sleep(0.3)
                alerta_vd = driver.switch_to.alert
                alerta_vd.accept()
            except:
                try:
                    driver.find_element(By.CSS_SELECTOR, 'input#DSP_BCT_CTL_TBL_BUSINESS_UNIT').clear()
                    break
                except:
                    esperar_carregamento_pagina()

        driver.find_element(By.CSS_SELECTOR, 'input#DSP_BCT_CTL_TBL_BUSINESS_UNIT').send_keys(cd)
        driver.find_element(By.CSS_SELECTOR, 'input[value="Adicionar"]').click()

        sleep(0.3)
        input_departamento = procurar.until(EC.element_to_be_clickable(mark=(By.CSS_SELECTOR, 'input[id="DSP_BCT_CTL_TBL_DSP_DP_RESP_CHR"]')))
        sleep(0.3)
        driver.execute_script(f"arguments[0].value = '{departamento_responsavel}';", input_departamento)
        sleep(0.3)

    def verificar_timeout():
        """
            Verifica se o tempo de espera do sistema PeopleSoft expirou.
        """
        
        if 'sub-frame-error-details' in driver.page_source:
            print('Time Out encontrado')
            return True # Erro na página, TIMEOUT

    def encontrar_iframe():
        """ 
            Encontra o iframe onde estão contidos os elementos a serem interagidos 
        """

        while True:
            try:
                iframe = driver.find_element(By.CSS_SELECTOR, 'frame[name="TargetContent"]')
                sleep(0.1)
                driver.switch_to.frame(iframe)
                sleep(0.1)
                break
            except:
                if verificar_timeout():
                    print('Timeout') ######################### EXCLUIR LINHA E REINICIAR LOOP #########################
                    break
                sleep(0.2)

    def esperar_carregamento_pagina():
        """
            Loop infinito para verificar se o ícone de processando do people está visível na página.
            A propriedade do elemento visibility encerra o loop com os valores: 
            'visible' significa que o ícone de processamento está visível (continua no loop), 'hidden' está oculto (encerra o loop).
        """

        while True:
            try:
                icone_processando = driver.find_element(By.CSS_SELECTOR, 'div[id="WAIT_win1"]')
                sleep(0.1)
                if icone_processando.value_of_css_property('visibility') == 'hidden':
                    sleep(0.1)
                    if not verificar_timeout():
                        sleep(0.1)
                        return True
                    else:
                        print('Timeout') ######################### EXCLUIR LINHA E REINICIAR LOOP #########################
                        break
                else:
                    continue
                
            except UnexpectedAlertPresentException:
                # print('Existe Alerta na página')
                try:
                    alert = driver.switch_to.alert
                    # print('Consegui associar o alerta')
                    sleep(0.3)
                    alert.accept() if not 'Excluir linhas atuais' in alert.text else sleep(0.3)
                except NoAlertPresentException:
                    sleep(0.3)
                return False


            except NoSuchElementException: # Esse ícone sempre está presente no frame, mesmo quando não está sendo processado.
                encontrar_iframe()
            
            except:
                sleep(0.1)

    def excluir_linha(linha):
        """
            Exclui a última linha inserida.
        """

        linha_antes_de_excluir = linha

        while True:
            
            try:
                botao_excluir_linha = procurar.until(EC.element_to_be_clickable(mark=(By.CSS_SELECTOR, 'a[id="DSP_BCT_DTL_TBL$delete$0$$0"]')))
                sleep(0.3)
            except:
                continue

            try:
                botao_excluir_linha.click()
                sleep(0.3)
                alerta_exclusao = driver.switch_to.alert
                if 'Excluir linhas atuais' in alerta_exclusao.text:
                    sleep(0.3)
                    alerta_exclusao.accept()
                    esperar_carregamento_pagina()
                    try:
                        linha_apos_exclusao = int(driver.find_element(By.CSS_SELECTOR, 'span.PSGRIDCOUNTER').text.split(' ')[0].strip())
                        if linha_antes_de_excluir > linha_apos_exclusao:
                            break
                        if linha_apos_exclusao == 1:
                            break
                    except:
                        sleep(0.3)

            except NoAlertPresentException:
                sleep(0.3)

    def adicionar_nova_linha(linha, skus_total):
        """
            Adiciona uma nova linha.
        """
        esperar_carregamento_pagina()
        if linha == skus_total:
            return False
        else:
            return True

    def validar_campos_preenchidos():
        """
            Verifica se todos os campos obrigatórios estão preenchidos corretamente,
            ou se todos os campos foram validados pelo people
        """

        while True:
            if not esperar_carregamento_pagina():
                return False
            else:
                return True        

    def preencher_lote(linha):
        """
            Preenche lote do item.
        """
        esperar_carregamento_pagina()

        while True:
            try:
                botao_lote = driver.find_element(By.CSS_SELECTOR, 'input[id="DSP_AJUSTIN_WRK_DSP_SELEC_LOTE$0"]')
                sleep(0.3)
                break
            except:
                esperar_carregamento_pagina()

        if botao_lote.get_property('disabled') == False:
            botao_lote.click()
            esperar_carregamento_pagina()

            for i in range(2):
                botao_classificar_validade = driver.find_element(By.NAME, 'DSP_AJUSTIN_LOT$srt3$0')
                sleep(0.3)
                driver.execute_script('arguments[0].click();', botao_classificar_validade)
                esperar_carregamento_pagina()
        
            driver.find_element(By.CSS_SELECTOR, 'input[id="DSP_AJUSTIN_LOT_QTY_AVAILABLE$0"]').send_keys(str(df.at[linha, 'Qtd']))
            driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="OK"]').click()


    def inserir_itens(df):
        """
            Insere os itens na página de transferência de local.
        """

        linha_anterior = 0

        for linha_item in df.index:
            
            while True: # Captura a linha atual da tabela people
                esperar_carregamento_pagina()
                linha_atual = int(driver.find_element(By.CSS_SELECTOR, 'span.PSGRIDCOUNTER').text.split(' ')[0].strip())
                if linha_atual > linha_anterior:
                    linha_anterior = linha_atual
                    break
            
            # Definir campos que serão preenchidos
            input_item = driver.find_element(By.CSS_SELECTOR, 'input[id="DSP_BCT_DTL_TBL_INV_ITEM_ID$0"]')
            input_qtd = driver.find_element(By.CSS_SELECTOR, 'input[id="DSP_BCT_DTL_TBL_QTY$0"]')
            input_area = driver.find_element(By.CSS_SELECTOR, 'input[id="DSP_BCT_DTL_TBL_STORAGE_AREA$0"]')
            input_nv1 = driver.find_element(By.CSS_SELECTOR, 'input[id="DSP_BCT_DTL_TBL_STOR_LEVEL_1$0"]')
            input_nv2 = driver.find_element(By.CSS_SELECTOR, 'input[id="DSP_BCT_DTL_TBL_STOR_LEVEL_2$0"]')
            input_dropdown_motivo = Select(driver.find_element(By.CSS_SELECTOR, 'select[id="DSP_BCT_DTL_TBL_DSP_RETORNO_DV$0"]'))

            # Preencher via script os campos do item
            driver.execute_script(f"arguments[0].value = {str(df.at[linha_item, 'Item'])};", input_item)
            driver.execute_script(f"arguments[0].value = {str(df.at[linha_item, 'Qtd'])};", input_qtd)
            driver.execute_script(f"arguments[0].value = '{area}';", input_area)
            driver.execute_script(f"arguments[0].value = '{nv1}';", input_nv1)
            driver.execute_script(f"arguments[0].value = '{nv2}';", input_nv2)
            input_dropdown_motivo.select_by_visible_text(motivo)
            
            if not validar_campos_preenchidos():
                excluir_linha(linha=linha_atual)

                linha_anterior -= 1
                if adicionar_nova_linha(linha=linha_anterior, skus_total=df.shape[0]) and linha_anterior !=0 and linha_item+1 < df.shape[0]:
                    driver.find_element(By.ID, 'DSP_BCT_DTL_TBL$new$0$$0').click()
                continue

            # Preencher o campo código do motivo de transferência
            while True:
                try:
                    input_cod_motivo = driver.find_element(By.CSS_SELECTOR, 'input[id="DSP_BCT_DTL_TBL_DSP_CODMOV_CHR$0"]')
                    sleep(0.1)
                    if input_cod_motivo.get_attribute('value') == '':
                        driver.execute_script(f"arguments[0].value = '{cod_motivo}';", input_cod_motivo)
                    break        
                except StaleElementReferenceException:
                    esperar_carregamento_pagina()
                    continue
            
            preencher_lote(linha=linha_item)

            if adicionar_nova_linha(linha=linha_anterior, skus_total=df.shape[0]):
                driver.find_element(By.ID, 'DSP_BCT_DTL_TBL$new$0$$0').click()

    def salvar_doc():
        """
            Salvar documento.
        """

        botao_salvar = procurar.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[id="#ICSave"]')))
        sleep(0.3)

        while True:
            try:
                botao_salvar.click()
                sleep(0.3)
                esperar_carregamento_pagina()
                numero_doc = procurar.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.PSEDITBOX_DISPONLY')))
                sleep(0.3)
                if  numero_doc.text != 'NEXT':
                    break
            except:
                esperar_carregamento_pagina()


    driver = webdriver.Chrome()
    procurar = WebDriverWait(driver=driver, timeout=60, poll_frequency=1)
    driver.implicitly_wait(10)

    fazer_login_people(usuario=usuario, senha=senha)
    encontrar_iframe()
    esperar_carregamento_pagina()
    preencher_cabecalho(cd=cd, departamento_responsavel=departamento_responsavel)

    df = auxiliar.df

    inserir_itens(df=df)
    salvar_doc()
