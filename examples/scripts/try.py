from icare_nlp.object_qa import ObjectQA

obj_qa=ObjectQA()
question="书包喺邊？"
target=obj_qa.get_short_expression_bert(question)