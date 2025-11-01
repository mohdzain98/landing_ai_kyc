<a id='1c4bfcbd-1766-4d87-b0a6-75939465110a'></a>

CAPTURING DEMAND TRANSFERENCE IN RETAIL - A STATISTICAL APPROACH

<a id='60f1976e-c328-495e-97fd-1a0ea9fb6873'></a>

**Omker Mahalanobish**
Statistical Analyst, Walmart Labs, Bengaluru, India
omker.mahalanobish@walmart.com

<a id='0b22169f-ca52-40d2-a972-78c8b99318c9'></a>

**Souraj Mishra**
Statistical Analyst, Walmart Labs, Bengaluru, India
souraj.mishra@walmart.com

<a id='51a26a00-9c2e-4c0e-8f41-422f284e222f'></a>

**Amlan Das**
Statistical Analyst, Walmart Labs, Bengaluru, India
amlan.das@walmart.com

<a id='34de82e8-7f98-4f94-bcbe-e168caee7466'></a>

Subhasish Misra*
Associate Data Scientist, Walmart Labs, Bengaluru, India
subhasish.misra@walmart.com

<a id='15c3ec65-9567-407a-a5f0-1608fd1935da'></a>

## Background:

While an item substitution measure provides for the direction, **demand transference** quantifies the magnitude of demand that may get transferred to an item a) When its substitute is deleted b) When it is introduced in a store and cannibalizes on similar items.

<a id='a63a1d48-9c6e-4c2b-83f8-ed2cb5ee6e51'></a>

This, hence, is an important input into assortment optimization. If an item is predicted to exhibit a good extent of transference **then we may be more certain of deleting it** (provided, it is less than an average performer in terms of sales). Conversely, we should be careful of deleting a very incremental item (with low demand transference) – since we'll be losing on a bulk of its demand.

<a id='4aa94667-9388-4e93-9ddf-1fe40fb91e6a'></a>

Note that transference is not explicitly observed, it's latent. Our methodology explains how we capture it.

<a id='d56c305b-2e60-448d-b911-ae801919978c'></a>

**Method:**
**Data:** POS, promotions & item attribute data is harnessed for this process.

<a id='5cdd30e4-1208-4d74-ac7f-7284e3659c58'></a>

## Modeling:

* Regression models (in a longitudinal setup) are used to estimate demand for an item – among other explanatory variables we have one that accounts for cannibalization effect of similar items.
* The cannibalization term uses the attribute data to calculate item similarity. Its value changes depending on presence/absence of similar items and is the instrument through which demand transference seeps into this model.

<a id='fa889e17-3ead-485f-af25-146f3d2cf442'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='03835f8f-9328-4027-b0de-0eb58f6920c3'></a>

- The modeling process is designed to automatically take care of complications such as multicollinearity and sundry regression violations.
- Since each store is unique in terms of the consumer demand pattern these models have been estimated at a store x substitutable community level.
- This means that for a category with 10 + substitutable community, we are estimating 10 * 4000 + = 40000 + models using parallelization techniques in Hadoop.

<a id='bef900a6-bd9b-4829-b44c-67f7d0fdbd4a'></a>

In conclusion, these models predict the extent of transference (i.e. if an item "i₁" in the pre-delete scenario was selling 100 units, then what amount of its demand would get transferred to its substitutes, say, "i₂", "i₃", "i₄"). All this, at an individual store level as well as the overall US.

<a id='c74a0638-0471-4aef-a9aa-f8d20eb2e595'></a>

**Expected outcome:**

The methodology has been successfully tested for multiple foods and consumable categories, as well as general merchandising categories in the US – efforts are on towards making this one of the processes of estimating demand transference. The entire process, despite involving sophisticated modeling has been **scaled (across all stores)**, **automated and productized** as an easy to use manner for the business user.

<a id='c06c342f-3992-471e-8fb0-2c992f376607'></a>

**Keywords:** *Regression, Cannibalization, Retail, Parallelization, Forecasting*

<a id='54b40b44-c527-457d-a17a-145cadaf34aa'></a>

# 1. INTRODUCTION
Assortment is a key element of a retailer's marketing mix. It differentiates a retailer from its competitors and has a very strong influence on retail sales. Retailers face the problem of selecting the assortment that maximizes category profitability, without sacrificing customer satisfaction.

<a id='36c8f343-53fc-4395-8fcd-a2dc79e26cd2'></a>

Although some headway has been made in the context of assortment optimization, practitioners and academics agree that more research is needed to provide feasible solutions to realistic assortment problems. Specifically, the challenge of assortment optimization is compounded by the fact that the demand for an item cannot be assumed to be fixed; it is instead affected by the presence of other items as a result of product substitution.

<a id='dc7d8629-be80-49c3-9b99-bfffc2d2b064'></a>

One of the important challenge is to account for similarity effects: an item is a stronger substitute for similar items than it is for dissimilar items. Demand is also driven by own- and cross-marketing mix instruments such as price, promotion and by heterogeneous preference across stores. Capturing these aspects in a response model is further complicated by the fact that assortments and prices observed in empirical data are unlikely to be exogenous. Finally, retailers have to decide about not only the assortment, but also about the pricing, and these decisions need to be customized at a store level.

<a id='b3b2d884-67a5-45aa-a3d6-c356d012d012'></a>

In the process of optimizing the store assortment, it is important to understand the process of demand transference. Demand transference is defined as the process of transfer of demand among the items in a store, once a change in assortment is realized.

<a id='7196ffcc-a59f-4fac-b3a9-e9634f5a1fa6'></a>

In a store, for a given category, there may be two realizations of an assortment change :
1. When one or more items are dropped from the assortment, customers who intended to buy any of the dropped items, might either choose to opt for another 'substitutable' item or walk away from the store, without a purchase.

<a id='b7e39c73-1e40-47c6-8649-996fe62804b3'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='b819389a-5d79-4103-a828-ad8c34891e7d'></a>

2. When one or more items are introduced into the assortment, customers who purchased any of the new items, might either buy the new item out of impulse or replace purchasing an existing item with the new item.

<a id='5128dfb0-4609-4ed5-a21d-3172eb8fb72a'></a>

A better understanding of this underlying process would help in identifying the optimum assortment for the particular category in the particular store. In this paper, we aim to model the mechanism of demand transference so as to optimize the store assortment, for the category.

<a id='dec3afb7-ad40-4b93-8a10-5377266a6113'></a>

## 2. LITERATURE REVIEW
This section briefly discusses about the studies in place related to assortment selection / optimization.

<a id='344ffaef-ec2a-4ce4-a4b8-07a3235d9452'></a>

The common points among the available literatures is that they all look to optimize the assortment, based on maximizing cost function (usually sales or profit). We here would only restrict ourselves towards those studies which deal with the item attributes along with the scanner data.

<a id='684ed44f-7aaa-470a-8355-2d6d3ac5ff7a'></a>

Among the available articles, Fisher and Vaidyanathan (Fisher et al., 2009) look into selecting the optimum number of items from the available lot, to maximize sales. They have defined an approach, in which they view a item as a set of attribute values, use sales history of the items currently carried by the retailer to estimate the demand for each of the attribute values and from this, the demand for any potential item currently not carried by the retailer. They also introduce a model of substitution behavior, estimate the parameters and consider the impact of substitution in choosing assortment.

<a id='5079de30-accf-4a56-ab96-1680c5a5ef43'></a>

Kök and Fisher (2007), also tread similar lines wherein they study an assortment planning model in which consumers might accept substitutes when their favorite product is unavailable. They develop an algorithmic process to help retailers compute the best assortment for each store, by estimating the parameters of substitution behavior and demand for products at a store, including products that have not been carried previously in that store. Finally, they propose an iterative optimization heuristic to solve the assortment planning problem.

<a id='300c593f-d5f7-4119-bbe4-047f571b6501'></a>

Other articles like Rooderkerk et al., (2013) look into price optimization along with promotion and shelf space optimization. Herein, they adopt a scalable assortment optimization method that allow for theory based substitution patterns and cross marketing mix effects. For the optimization part, they propose a large neighborhood search heuristic methodology.

<a id='f65297ab-3ecd-4dcc-9d7c-c989d00d2af0'></a>

Our study though on similar lines, addresses an entirely different aspect of assortment study. This is more of scenario based, to understand how the store assortment performs when a change in the store assortment is realized. Basically, we help the retailer to decide which items to drop from the assortment, by helping him understand where the demand of the deleted item would flow to and in what magnitude. The retailer also gets a glimpse of additional incremental demand as well as the magnitude and direction of cannibalization that might be realized when additional items are added to the assortment. In the process of obtaining these insights, he also gets an understanding as to how the items in the new assortment will perform in the future.

<a id='fa5162e4-b716-437c-81b9-37b1326138af'></a>

### 3. METHODOLOGY
Demand is a latent feature, which can be experienced but not explicitly observed. Thus, modeling of demand and validation of the same becomes difficult. The nearest proxy to demand is sales. So, here we try to model the sales of each of the products offered in an assortment.

<a id='42ee07af-ca3e-4fd6-a0e5-921ef3e37160'></a>

Our methodology consists of a sales model, described in section 3.1 and a predictive algorithm based on the sales model, as described in section 3.2.

<a id='4cb0ef3e-238e-4184-a1b2-a48bc464e970'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='08acc261-0e15-49fc-aee7-948786c1a1a6'></a>

### 3.1. Sales model

Before formulating the model, we look at a significant challenge encountered while developing the sales model: modeling store level UPC sales on attributes. UPC (Universal Product Code) is used to identify trade items in stores across different retailers and markets. UPC is aggregation of items which can vary across different regions.

<a id='447dc885-fbcd-458c-9a83-4c0d37b45d32'></a>

### 3.1.1. Modeling framework
To model UPC sales at a store level, we chose store-level scanner data, as it provides a holistic view of the available assortment in the store. An example of the input data is provided in Table 1 under section 4.1. Our approach of modeling UPC sales on UPC attributes is motivated by the assertion that customers do not form preference of each individual UPC in a product category but that these preferences are derived from the preferences for the underlying attributes (e.g., size, brand, flavor, etc.). Theoretical justification of the same is available in economics (Lancaster, 1971) and psychology (Fishbein, 1967).

<a id='f651fe84-032f-49d3-a41b-b3d31c9cbda7'></a>

Our model thus takes into account the UPC attributes, in order to model UPC sales. Apart from the UPCs own attributes, attributes of other available UPCs would also affect the sales. We thus incorporate variables to account for a UPCs attribute similarity as well as cross attribute similarity with the other UPCs in the assortment.

<a id='ae416f67-034b-4798-959b-5ed0aeb98d25'></a>

### 3.1.2. Modeling formulation
We would now develop the attribute based model and highlight the role similarity variables play. While modeling UPC sales at a store level, we allow for flexible substitution patterns, and non-linear effects by starting with a log-log model (Rooderkerk et al., 2013), similar to the SCAN*PRO model (Wittink et al., 1988):

log($S_{kti}$) = $\underbrace{\alpha_{ki}}_{A}$ + $\underbrace{\beta.log(P_{kti})}_{B}$ + $\underbrace{\sum_{m \in A} \gamma_{kmti}}_{C}$ (1)

<a id='e3311eab-0693-4356-ae66-25672f8a2296'></a>

where,

$S_{kti}$ = unit sales of UPC $k \in \{1, 2, ..., K\}$ in week $t \in \{1, 2, ..., T\}$ in store $i \in \{1, 2, ..., n\}$;

$\alpha_{ki}$ = UPC-store intercept for UPC $k \in \{1, 2, ..., K\}$ in store $i \in \{1, 2, ..., n\}$;

$P_{kti}$ = price of UPC $k \in \{1, 2, ..., K\}$ in week $t \in \{1, 2, ..., T\}$ in store $i \in \{1, 2, ..., n\}$;

$\gamma_{kmti}$ = similarity score of UPC $k \in \{1, 2, ..., K\}$, for attribute $m \in \mathcal{A}$, in week $t \in \{1, 2, ..., T\}$ in store $i \in \{1, 2, ..., n\}$;

$\mathcal{A}$ = set of all attributes, evaluated for all UPCs in a product category;

<a id='e8ac1f70-b95c-4edd-bdc7-dfd04f4e4f8d'></a>

Further, $\alpha_{ki}$ may be replaced by strictly store level intercepts along with attribute dummies such that

$\alpha_{ki} = \underbrace{\alpha_i}_{A} + \underbrace{\sum_{m \in A} \sum_{l=1}^{m_l} A_{kml}}_{B}$ (2)

<a id='2aa04133-b747-4717-9e77-b76013f848cf'></a>

where,

&nbsp;&nbsp;&nbsp;&nbsp;A_kml = 1 if UPC k possesses level l of attribute m ∈ A, and 0 otherwise, if m is nominal

&nbsp;&nbsp;&nbsp;&nbsp;A_kml = the realization of attribute m ∈ A, if m is metric

<a id='245a3e8d-5ebb-4f9c-ad90-f51eaf6b4736'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='accdb2e0-1768-4aa4-9bb1-1633529cc45b'></a>

### 3.1.3. Attribute similarity score
The similarity score of UPC _k_, for a nominal or metric attribute _m_, in week _t_, in store _i_ is defined such that it varies between 0 (minimum similarity) and 1 (maximum similarity), and also reflects the similarity of UPC _k_ relative to the distribution of attribute _m_ in the entire available assortment.

<a id='f0019c10-2329-4a02-9565-b55d9ef53215'></a>

Let $SIM_{kk'mti}$ denote the magnitude of similarity between UPC $k$ and UPC $k'$ with respect to attribute $m$ in store $i$ in week $t$.

<a id='42bfd214-f293-4074-b517-7c407bb19d8a'></a>

Further to the above discussed features of similarity, if UPC k and UPC k' share the same level of nominal attribute m, then the perceived similarity of UPC k and UPC k' should be stronger when their shared attribute level occurs less frequently (Goodall, 1966). We obtain all the above, by defining :

<a id='e64820df-cbab-498a-8bc0-ca156a3a967f'></a>

$$SIM_{kk'mti} = I\{A_{k'm} = A_{km}\}. \left(1 - \frac{1}{N_{ti}} \sum_{k''=1, x_{k''ti}=1}^{K} I\{A_{k''m} = A_{km}\} \right) \quad (3a)$$

<a id='5be6f323-95da-4948-b2c9-80e21cbfb54c'></a>

if attribute _m_ is nominal, where,

I{·} = an indicator function which takes the value 1 if its argument holds, 0 otherwise;

_A_<sub>_km_</sub> = the level attained by UPC _k_ on attribute _m_ such that _A_<sub>_km_</sub> = _l_ ⇔ _A_<sub>_kml_</sub> = 1;

_N_<sub>_ti_</sub> = the number of UPCs present in week _t_ in store _i_;

_x_<sub>_kti_</sub> = 1, if UPC _k_ was available in store _i_, for at least 1 day in week _t_; else 0.

<a id='5485ca74-f8b9-49fd-b9ce-c122258ef506'></a>

Table 3 in section 4.2 illustrates how this would work for a Brand attribute.

<a id='d8120f48-fe21-4c2b-a199-93dc5f0f86dc'></a>

On the other hand, the similarity of UPC k and UPC k', with respect to a metric attribute m, is perceived to be more if there exists fewer UPCs with attribute values between the attribute values of UPC k and UPC k'. This is obtained by defining:

<a id='a175f193-7a75-498a-b5bd-da0c7445fb33'></a>

$$SIM_{kk'mti} = 1 - \frac{1}{N_{ti}} \cdot \sum_{\substack{k''=1 \\ x_{k''ti}=1}}^{K} I\{\min(A_{km}, A_{k'm}) \leq A_{k''m} \leq \max(A_{km}, A_{k'm})\} \quad (3b)$$

<a id='3f94f733-a6f7-4b52-8b69-76bdff4d1ca3'></a>

if attribute _m_ is metric.
This definition is numerically illustrated for Weight attribute in Table 5 in section 4.2.

<a id='88dc517e-fe4b-4e88-b5c5-0ba2b4bad70e'></a>

Once we have described the measure of similarity for UPC k and UPC k', we may now formulate the similarity score of UPC k for attribute m in week t in store i as:

$\gamma_{kmti} = mean^*_{k'\neq k} (SIM_{kk'mti})$

(4)

<a id='bb651cb4-4e33-418a-a79d-69de57c39ea9'></a>

where,
$mean^*(.) = \text{Arithmetic Mean of the non-zero elements of the argument, if attribute } m \text{ is}$
nominal, usual Arithmetic Mean otherwise.

<a id='08f8db14-111c-48db-bd7e-9bce2c2c5d41'></a>

### 3.1.4. Model implementation
The model described in this paper, is best implemented when modeled category wise. Now, each category has properties of its own and consists of widely different varieties of UPCs. The two major category properties that is observed is as follows:

<a id='90977304-b0e8-4409-9758-e62486e0b729'></a>

1. Demand might get transferred to any and every UPC of the category and

<a id='b596cfee-19b4-4af0-9c7a-f12b7c63d86f'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753
Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='aa0b568c-1cde-4d95-9d52-98a165643c99'></a>

2. Transfer of demand is restricted only within mutually exclusive and exhaustive set of substitutable groups, which are very different from each other (further discussed in section 4.3).

<a id='cfa6763e-e8e5-4175-b7af-3111c302f814'></a>

For case 2, one may carry on the same analysis over each substitutable group, as if assuming it to be a small sized category of sorts.

<a id='d1bb086d-8249-4939-abb9-4426967ef5f5'></a>

Since we have formulated a linear regression as mentioned in (1), all regression sanity checks have been taken care of and the final model thus only consists of the uncorrelated and significant regressors among the ones mentioned in (1).

<a id='6cf331a4-1c8d-4f79-801a-5681cc57257f'></a>

## 3.2. Predictive algorithm
We would now look into how to predict the magnitude of demand transference and the walkoff rate.
Define

<a id='d7b7353e-448d-48f9-90e6-8e8fc5659e81'></a>

A_i : the training assortment of store i;
A'_i : the assortment of store i after the assortment change;

<a id='901a1ed9-d826-46b4-a250-adefdba02875'></a>

Now, for every UPC in A_t, we can easily obtain the predicted weekly unit sales from the model as explained in (1).

<a id='a60c6e09-3d70-4b28-b341-cddad136cebd'></a>

Also, the values of parts A and B in (1) are independent of the store assortment (assuming there is no change in price in any of the items in Aᵢ) and thus doesn't change. It suffices to compute these values only for those UPCs that have been introduced in A'ᵢ but were not a part of Aᵢ. Part C in (1) directly depends upon the current assortment in store and hence the similarity score is recalculated for each UPC in the new assortment. Once we have all the required information, the predicted weekly unit sales of every UPC in Aᵢ can be easily obtained.

<a id='75df8358-3b08-41ff-b8a5-d8918a07783c'></a>

Define,

$\hat{S}_{ki}$ = predicted weekly unit sales of UPC $k \in A_i$;

$\hat{S}'_{ki}$ = predicted weekly unit sales of UPC $k \in A'_i$;

<a id='83d7fedb-d1b0-48ab-9bb1-1abc30a95ce1'></a>

Therefore,

<a id='a4b7c153-d53c-42dc-bbed-0996bcd4d3e9'></a>

$\Delta S_{ki} = \hat{S}'_{ki} - \hat{S}_{ki}$, is the change in the weekly unit sales of UPC $k \in A_i \cap A'_i$.
But, $\Delta S_{ki} = \hat{S}'_{ki}$, if UPC $k \in A'_i \setminus A_i$

<a id='914626cd-1d03-4d2a-b3b4-4dfa205c70e4'></a>

### 3.2.1. Case of item deletion
Define $U_{del}$ = set of UPCs that have been deleted from $A_i$, and are not present in $A'_i$. Then,

<a id='9bde06a2-7d33-46ce-b9e9-5eb4ad4f3f0e'></a>

$\Delta_{kA'i}^{del} = \frac{\Delta S_{ki}}{\sum_{t \in u_{del}} \hat{S}_{ti}} . 100 \%$ (5a)

<a id='6fb5349d-12a7-40f0-a639-15c53ef89799'></a>

where,

<a id='c6ae5111-5fa8-4615-80d1-29225aa99219'></a>

$\Delta_{kA'_i}^{del}$ = demand of UPCs in $U_{del}$ transferred to UPC $k$, $\forall k \in A'_i$.

<a id='e7f3c562-da3d-47a4-b578-fe8b1752a07b'></a>

Herein, the walk-off rate is calculated as:
$ω_{A'_i}^{del} = 100 - \sum_{k \in A'_i} Δ_{kA'_i}^{del}$ (5b)

<a id='4302ac40-fa8e-4bba-b4a9-e6bda3305bc1'></a>

### 3.2.2. Case of item addition
Define, U_add = set of UPCs that have been added to A'_i, but were not a part of A_i. Then,

<a id='ad8a3254-a772-49ac-99fc-388e2c43da28'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='03fe00ce-59c8-43a7-887d-505987a236de'></a>

$$\Delta_{k A'_i}^{add} = \frac{|\Delta S_{ki}|}{\sum_{t \in u_{add}} \hat{S}_{ti}'} \cdot 100 \%$$ (6a)

<a id='2f01ad97-a001-4ab4-ace8-b7b999a615fe'></a>

where,

<a id='5cfbf3d0-1c7d-416a-b2d2-3fe7a66b7ec3'></a>

$\Delta_{kA'_i}^{add} = \text{demand of UPCs in } U_{add} \text{ cannibalized from UPC } k, \forall k \in A'_i.$

<a id='b6901034-1031-47ed-8cd0-0dc93bbc43e1'></a>

Herein, the incrementality is calculated as:

$$\omega_{A'_i}^{add} = 100 - \sum_{k \in A'_i} \Delta_{kA'_i}^{add} \quad (6b)$$

<a id='f71d4564-ebf2-4b6b-a665-5a493bede9d5'></a>

### 3.2.3. Case of both item deletion and item addition
In this case, it becomes difficult to identify separately, what amount of the change in the demand for UPC _k_, is due to the transfer of demand from the deleted UPCs and how much amount is due to cannibalization of the added UPCs. Further, there could even be some amount of demand transference towards the newly added UPCs as well.

<a id='779285c1-323e-4477-aa9d-9f88d26e9ced'></a>

Hence, one may separately consider the deletions and additions to obtain the demand transference measures.

<a id='fd6f7479-4f73-4c99-8d2a-cddad956e384'></a>

Therefore, we have

<a id='02eca9ef-0f5e-42cf-9617-4551808c3a35'></a>

$$\Delta_{K A'_i}^{add} = \frac{|\Delta S_{ki}| \cdot |\mathcal{U}_{add}|}{|\mathcal{U}_{del}| \cdot \sum_{t \in \mathcal{U}_{add}} \hat{S}_{ti}} \cdot 100 \%, \forall k \in A'_i \quad (7a)$$

<a id='3cd250ea-9e63-4685-8c60-f0cbfb1480cb'></a>

$$\Delta_{kA'i}^{del} = \frac{\Delta S_{ki} \cdot \frac{|U_{del}|}{|U_{add}|}}{\sum_{t \in U_{del}} \hat{S}_{ti}} \cdot 100\%, \quad \forall k \in A'_i \quad (7b)$$

<a id='250d2a15-51dd-44a2-b19a-807a06de2798'></a>

where,

$\Delta_{kA'_i}^{add}$ = demand of UPCs in $U_{add}$ cannibalized from UPC $k$, $\forall k \in A'_i$.

$\Delta_{kA'_i}^{del}$ = demand of UPCs in $U_{del}$ transferred to UPC $k$, $\forall k \in A'_i$.

<a id='dfae99cf-6231-4d58-a7bc-f363010b38be'></a>

In (7b),

$ΔS_{ki} = ΔS_{ki} · (1 - \sum_{t∈\mathcal{U}_{add}} \frac{Δ_{tA^i}^{add}}{100} · I\{k ∈ \mathcal{U}_{add}\})$ (7c)

<a id='8239a551-b3b6-4c1a-ad74-0b8585080585'></a>

Therefore, walkoff rate is:

$\omega_{A'_i}^{del} = 100 - \sum_{k \in A'_i} \Delta_{kA'_i}^{del}$

(7d)

<a id='55d070cb-941a-4b55-a7b5-de7e8b69bf54'></a>

and incrementality is defined as:

<a id='c872b223-5e0b-42cc-aaff-1ceda23a3a36'></a>

$$\omega_{A'_i}^{add} = 100 - \sum_{k \in A'_i} \Delta_{kA'_i}^{add} - \sum_{k \in \mathcal{U}_{add}} \Delta_{kA'_i}^{del} \quad (7e)$$

<a id='6398ac7b-cdec-442b-877b-ba9205834747'></a>

4. DISCUSSION

<a id='0d4133a1-b984-4d58-a784-75949e6eb76c'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753
Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='039b1d59-4ab6-4321-a4ad-ffc753c23cf7'></a>

Here, we will have a brief walkthrough of a sample input data for the algorithm along with the similarity calculation for the same.

<a id='d61136d3-276c-409d-bafb-d9abeddaa916'></a>

## 4.1. Scanner data and attribute data
Table 1 refers to a snapshot of the scanner data that we require to carry on with the analysis.
The snapshot here has been restricted to 4 UPCs, in 3 weeks and 1 store.

<a id='eb5b0b85-6f82-46d2-aef5-7e4b5da8593d'></a>

Table 1 Snapshot of the scanner data
<table id="7-1">
<tr><td id="7-2">Store No.</td><td id="7-3">UPC</td><td id="7-4">Week No.</td><td id="7-5">Units sold</td><td id="7-6">Dollar Sales</td><td id="7-7">Price</td><td id="7-8">Days available</td></tr>
<tr><td id="7-9">1</td><td id="7-a">UPC 1</td><td id="7-b">1</td><td id="7-c">2</td><td id="7-d">2.40</td><td id="7-e">1.20</td><td id="7-f">7</td></tr>
<tr><td id="7-g">1</td><td id="7-h">UPC 1</td><td id="7-i">2</td><td id="7-j">3</td><td id="7-k">3.55</td><td id="7-l">1.18</td><td id="7-m">7</td></tr>
<tr><td id="7-n">1</td><td id="7-o">UPC 1</td><td id="7-p">3</td><td id="7-q">2</td><td id="7-r">2.40</td><td id="7-s">1.20</td><td id="7-t">7</td></tr>
<tr><td id="7-u">1</td><td id="7-v">UPC 2</td><td id="7-w">1</td><td id="7-x">6</td><td id="7-y">4.50</td><td id="7-z">0.75</td><td id="7-A">6</td></tr>
<tr><td id="7-B">1</td><td id="7-C">UPC 2</td><td id="7-D">2</td><td id="7-E">7</td><td id="7-F">5.25</td><td id="7-G">0.75</td><td id="7-H">7</td></tr>
<tr><td id="7-I">1</td><td id="7-J">UPC 2</td><td id="7-K">3</td><td id="7-L">2</td><td id="7-M">1.60</td><td id="7-N">0.80</td><td id="7-O">7</td></tr>
<tr><td id="7-P">1</td><td id="7-Q">UPC 3</td><td id="7-R">1</td><td id="7-S">0</td><td id="7-T">0.00</td><td id="7-U"></td><td id="7-V">0</td></tr>
<tr><td id="7-W">1</td><td id="7-X">UPC 3</td><td id="7-Y">2</td><td id="7-Z">3</td><td id="7-10">4.50</td><td id="7-11">1.50</td><td id="7-12">3</td></tr>
<tr><td id="7-13">1</td><td id="7-14">UPC 3</td><td id="7-15">3</td><td id="7-16">1</td><td id="7-17">1.50</td><td id="7-18">1.50</td><td id="7-19">4</td></tr>
<tr><td id="7-1a">1</td><td id="7-1b">UPC 4</td><td id="7-1c">1</td><td id="7-1d">10</td><td id="7-1e">6.00</td><td id="7-1f">0.60</td><td id="7-1g">7</td></tr>
<tr><td id="7-1h">1</td><td id="7-1i">UPC 4</td><td id="7-1j">2</td><td id="7-1k">8</td><td id="7-1l">4.80</td><td id="7-1m">0.60</td><td id="7-1n">7</td></tr>
<tr><td id="7-1o">1</td><td id="7-1p">UPC 4</td><td id="7-1q">3</td><td id="7-1r">2</td><td id="7-1s">1.24</td><td id="7-1t">0.62</td><td id="7-1u">2</td></tr>
</table>

<a id='51790390-c7ae-4bba-a0e6-93e7a9a154bc'></a>

Table 2 Attribute information for UPCs in the snapshot
<table id="7-1v">
<tr><td id="7-1w">UPC</td><td id="7-1x">Brand</td><td id="7-1y">Weight (in gm)</td></tr>
<tr><td id="7-1z">UPC 1</td><td id="7-1A">Brand 1</td><td id="7-1B">200</td></tr>
<tr><td id="7-1C">UPC 2</td><td id="7-1D">Brand 1</td><td id="7-1E">180</td></tr>
<tr><td id="7-1F">UPC 3</td><td id="7-1G">Brand 1</td><td id="7-1H">200</td></tr>
<tr><td id="7-1I">UPC 4</td><td id="7-1J">Brand 2</td><td id="7-1K">150</td></tr>
</table>

<a id='ffc1d584-42e5-4b9a-94aa-6e516bd4ea94'></a>

**4.2. Computing the attribute similarity score**
As depicted in Table 2, there are two attributes to take care of viz. Brand (a nominal attribute) and Weight (a metric attribute).

<a id='6b2cc927-e95a-4cd1-bdf6-30d9aed5ea69'></a>

For attribute Brand, Brand 1 is present in 75% of the overall assortment, whereas Brand 2 is present in 25% of the overall assortment.

<a id='256c56c0-e6a2-48b4-ade3-31f0b25d2a78'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='d822ae3e-f2c1-4d29-aca6-64e5100a37d7'></a>

Hence, according to this example, the similarity scores for UPC 1 with respect to the nominal attribute Brand is demonstrated in Table 3 below:

<a id='dbf56dea-9601-48f9-8dca-a09bd9a1062c'></a>

Table 3 Week wise brand similarity score for UPC 1
<table id="8-1">
<tr><td id="8-2">Week No.</td><td id="8-3">Brand 1 presence</td><td id="8-4">Brand similarity score (γkmti)</td></tr>
<tr><td id="8-5">1</td><td id="8-6">66.67%</td><td id="8-7">0.33</td></tr>
<tr><td id="8-8">2</td><td id="8-9">75.00%</td><td id="8-a">0.25</td></tr>
<tr><td id="8-b">3</td><td id="8-c">75.00%</td><td id="8-d">0.25</td></tr>
</table>

<a id='171156f0-cd57-404b-bc78-7b922d31d668'></a>

Similarly, for the metric attribute Weight, similarity score of UPC 1 is seen to be as described in Table 5 below:

<a id='f236d3f4-9aa5-4e28-b306-cdafb62b3fe7'></a>

**Table 4** Weekly weight proximity percent for each UPC
<table id="8-e">
<tr><td id="8-f">UPC</td><td id="8-g">Week No.</td><td id="8-h">Weight proximity percent</td><td id="8-i">Weight similarity score</td></tr>
<tr><td id="8-j">UPC 2</td><td id="8-k">1</td><td id="8-l">66.67 %</td><td id="8-m">0.33</td></tr>
<tr><td id="8-n">UPC 2</td><td id="8-o">2</td><td id="8-p">75.00 %</td><td id="8-q">0.25</td></tr>
<tr><td id="8-r">UPC 2</td><td id="8-s">3</td><td id="8-t">75.00 %</td><td id="8-u">0.25</td></tr>
<tr><td id="8-v">UPC 3</td><td id="8-w">1</td><td id="8-x">–</td><td id="8-y">–</td></tr>
<tr><td id="8-z">UPC 3</td><td id="8-A">2</td><td id="8-B">75.00 %</td><td id="8-C">0.25</td></tr>
<tr><td id="8-D">UPC 3</td><td id="8-E">3</td><td id="8-F">75.00 %</td><td id="8-G">0.25</td></tr>
<tr><td id="8-H">UPC 4</td><td id="8-I">1</td><td id="8-J">100.00 %</td><td id="8-K">0.00</td></tr>
<tr><td id="8-L">UPC 4</td><td id="8-M">2</td><td id="8-N">100.00 %</td><td id="8-O">0.00</td></tr>
<tr><td id="8-P">UPC 4</td><td id="8-Q">3</td><td id="8-R">100.00 %</td><td id="8-S">0.00</td></tr>
</table>

<a id='74f99fb3-c442-4698-af6f-fd34f9680d6f'></a>

Therefore,
<table id="8-T">
<tr><td id="8-U" colspan="2">Table 5 Weekly weight similarity score for UPC 1</td></tr>
<tr><td id="8-V">Week No.</td><td id="8-W">Weight Similarity score</td></tr>
<tr><td id="8-X">1</td><td id="8-Y">0.165</td></tr>
<tr><td id="8-Z">2</td><td id="8-10">0.250</td></tr>
<tr><td id="8-11">3</td><td id="8-12">0.250</td></tr>
</table>

<a id='fc1d3418-5f6b-44b1-bcbf-e73e14d11e5a'></a>

### 4.3. Substitutable groups
A category can be divided into mutually exclusive and exhaustive groups of items, called substitutable groups. A substitutable group consists of items that are more likely to be substitutes of each other, than that of items in the other substitutable groups.

<a id='eda0743a-bb84-44c9-8ddc-2615a933b33f'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='17043bab-42b7-4edb-9733-ee7e3fbe7d22'></a>

We accomplish this segmentation into substitutable group by using a proprietary graph partition based algorithm.

<a id='29f1f5c9-0302-4ddf-93c5-9eb651ba5c2e'></a>

When, implemented for a substitutable group, the demand transfer algorithm restricts the transfer of demand within the same group; since by definition, there is very less probability of items in other groups to be proper substitutes.

<a id='34bf6406-757c-4be0-807c-ee60b8caaa8b'></a>

## 4.4. Parallelization techniques
The entire algorithm was executed in R, for a category with 7 substitutable groups, available in 4500 stores.

<a id='6f4252d7-6eb9-491c-a78a-55c878a48c9c'></a>

While *Hadoop streaming* was used to execute the algorithm over stores; for a store, the *mclapply* function (which uses forking technique) from *parallel* package was used to parallelize over substitutable groups.

<a id='fe17b6c4-47e3-4841-bba1-47c377d4b347'></a>

For a fixed store, the runtime in R (using forking via _mclapply_) is comparable to the runtime when executed in Python without any scaling up technique.

<a id='33c70148-d3e4-4d70-8979-b4d1b2c0af02'></a>

## 4.5. Results and success stories
This algorithm has been run for a variety of categories, both General Merchandise and Fast-Moving Consumer Goods (like Yogurt, Light Bulbs, Dish Soap, Utility Pants, Food Storage, etc.) and has been seen to be performing really well.

<a id='5a54daa1-a668-4160-9e3a-38ce2f95605b'></a>

The Mean Absolute Percentage Error for the model, when validated against observed assortment changes for the aforementioned categories, was almost always in the range of 4% to 13%.

<a id='aef5b20a-f97d-4822-ab77-0895ce480954'></a>

## 5. CONCLUSION
The problem of demand transference is an important one for any retailer. Obviously, the retailer cannot keep on carrying the same assortment over time. Market trends as well as the item performance, will always compel him to offer his customers the best assortment so as to maximize sales and customer satisfaction. Hence, it is better off to know from beforehand the magnitude of demand transference or cannibalization, that might be experienced with regards to a particular change in his assortment. Having a good understanding of the different scenarios will surely let him plan better than his competitors, and establish his stand in the market.

<a id='7e70692d-34af-4e96-9b69-d9d141f3ade5'></a>

Wrong choice of item deletion, might have severe repercussions in the form of:
1. churning of customer base which were loyal to the deleted product; or
2. churning of customer base, due to unavailability of proper substitutes of the deleted product in the available assortment.

<a id='9de2a9e4-8586-447e-9ee1-ab51d0c01e45'></a>

Similarly, wrong choice of item addition could also be detrimental in the form of the new item not attracting any incremental demand of its own, but is only cannibalizing the demand of the other available items in the assortment, thus not doing any significant good to the retailer.

<a id='665fdc0c-966b-4ee9-9687-000cb0c3104c'></a>

This study has been aimed to help the retailer address these basic problems of assortment.

<a id='ddf66cab-4fb8-4e75-9f21-2acd10382378'></a>

## 6. REFERENCES
Fishbein M, ed. (1967) *Attitude and Prediction of Behavior* (John Wiley & Sons, New York).
Fisher ML, Vaidyanathan R (2009) An Algorithm and Demand Estimation Procedure for Retail Assortment Optimization. The Wharton School, Philadelphia, Pennsylvania.
Goodall DW (1966) A new similarity index based on probability. *Biometrics* 22(4):882–907.

<a id='4ac48b7a-53ac-485b-a20a-f0bc24557c86'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='99dd86e5-f3bd-4a22-b78d-6f234704fa00'></a>

Kök, G., M. L. Fisher. 2007. Demand Estimation and Assortment Optimization under
Substitution: Methodology and Application. Operations Research 55(6) 1001–1021.
Lancaster K (1971) Consumer Demand: A New Approach (Columbia University Press, New
York).

<a id='dd95374c-5e16-4a6d-a608-149b074e6f9a'></a>

Rooderkerk RP, van Heerde HJ, Bijmolt TH (2011) Optimizing Retail Assortments. *Marketing Science* 32(5):699–715.

<a id='b4e1f5c6-dfdd-4ec0-886a-fec7264bf921'></a>

Wittink DR, Addona MJ, Hawkes W, Porter JC (1988) SCAN*PRO:The estimation, validation, and use of promotional effects based on scanner data. Working paper, Cornell University, Ithaca, NY.

<a id='925b2a91-a863-4035-be36-e4cfa72af868'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753