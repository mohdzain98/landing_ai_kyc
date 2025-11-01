<a id='09a0f366-a819-4aef-b71d-563a00a7eda3'></a>

CAPTURING DEMAND TRANSFERENCE IN RETAIL - A STATISTICAL APPROACH

<a id='ae14062d-e909-4091-aa2a-d16a55ee69ca'></a>

**Omker Mahalanobish**
Statistical Analyst, Walmart Labs, Bengaluru, India
omker.mahalanobish@walmart.com

<a id='da00be18-def5-4386-8370-8403e6b6fd9d'></a>

**Souraj Mishra**
Statistical Analyst, Walmart Labs, Bengaluru, India
souraj.mishra@walmart.com

<a id='cbd18c9e-0a47-4856-a7d6-a946527a83f4'></a>

**Amlan Das**
Statistical Analyst, Walmart Labs, Bengaluru, India
amlan.das@walmart.com

<a id='a8278c21-358a-4453-b08b-3d0fed59f5a6'></a>

Subhasish Misra*
Associate Data Scientist, Walmart Labs, Bengaluru, India
subhasish.misra@walmart.com

<a id='7cca309c-d205-4c10-96b9-c8bb3fb4edb3'></a>

## Background:

While an item substitution measure provides for the direction, **demand transference** quantifies the magnitude of demand that may get transferred to an item a) When its substitute is deleted b) When it is introduced in a store and cannibalizes on similar items.

<a id='a4ba3890-c3fd-416c-b017-aa0c331ed69f'></a>

This, hence, is an important input into assortment optimization. If an item is predicted to exhibit a good extent of transference **then we may be more certain of deleting it** (provided, it is less than an average performer in terms of sales). Conversely, we should be careful of deleting a very incremental item (with low demand transference) – since we'll be losing on a bulk of its demand.

<a id='fa5dbe1f-d06b-4a36-9063-ca560986bfbb'></a>

Note that transference is not explicitly observed, it's latent. Our methodology explains how we capture it.

<a id='d5f8ca7f-51a4-4ac2-87db-6a2c7f2872ec'></a>

**Method:**
**Data:** POS, promotions & item attribute data is harnessed for this process.

<a id='8aec2828-7c45-4090-9341-b60b01ec7632'></a>

## Modeling:

* Regression models (in a longitudinal setup) are used to estimate demand for an item – among other explanatory variables we have one that accounts for cannibalization effect of similar items.
* The cannibalization term uses the attribute data to calculate item similarity. Its value changes depending on presence/absence of similar items and is the instrument through which demand transference seeps into this model.

<a id='eee235a6-9fd9-471b-9cce-fb4dac83200e'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='2b2f167c-69f2-41cf-99c8-d92b1009f58a'></a>

- The modeling process is designed to automatically take care of complications such as multicollinearity and sundry regression violations.
- Since each store is unique in terms of the consumer demand pattern these models have been estimated at a store x substitutable community level.
- This means that for a category with 10 + substitutable community, we are estimating 10 * 4000 + = 40000 + models using parallelization techniques in Hadoop.

<a id='ce2195c2-0f70-4bb5-9c77-6741c700e5f4'></a>

In conclusion, these models predict the extent of transference (i.e. if an item "i₁" in the pre-delete scenario was selling 100 units, then what amount of its demand would get transferred to its substitutes, say, "i₂", "i₃", "i₄"). All this, at an individual store level as well as the overall US.

<a id='845e872e-c575-483d-8d7d-c5ada5fa6d0a'></a>

**Expected outcome:**

The methodology has been successfully tested for multiple foods and consumable categories, as well as general merchandising categories in the US – efforts are on towards making this one of the processes of estimating demand transference. The entire process, despite involving sophisticated modeling has been **scaled (across all stores)**, **automated and productized** as an easy to use manner for the business user.

<a id='0e94e24d-25a7-40b2-b973-d672c1500c3c'></a>

**Keywords:** *Regression, Cannibalization, Retail, Parallelization, Forecasting*

<a id='a7c9a321-9da0-4ee6-a221-d6c2de6f528c'></a>

# 1. INTRODUCTION
Assortment is a key element of a retailer's marketing mix. It differentiates a retailer from its competitors and has a very strong influence on retail sales. Retailers face the problem of selecting the assortment that maximizes category profitability, without sacrificing customer satisfaction.

<a id='febc9ffb-5d55-4dae-8e5c-4662a1142fb0'></a>

Although some headway has been made in the context of assortment optimization, practitioners and academics agree that more research is needed to provide feasible solutions to realistic assortment problems. Specifically, the challenge of assortment optimization is compounded by the fact that the demand for an item cannot be assumed to be fixed; it is instead affected by the presence of other items as a result of product substitution.

<a id='54d25708-ceae-444b-8dc8-14ca68ae25a6'></a>

One of the important challenge is to account for similarity effects: an item is a stronger substitute for similar items than it is for dissimilar items. Demand is also driven by own- and cross-marketing mix instruments such as price, promotion and by heterogeneous preference across stores. Capturing these aspects in a response model is further complicated by the fact that assortments and prices observed in empirical data are unlikely to be exogenous. Finally, retailers have to decide about not only the assortment, but also about the pricing, and these decisions need to be customized at a store level.

<a id='4c75dfd2-cc85-4113-858f-b6eed2ec6156'></a>

In the process of optimizing the store assortment, it is important to understand the process of demand transference. Demand transference is defined as the process of transfer of demand among the items in a store, once a change in assortment is realized.

<a id='e0ff0c3f-b979-4c81-9d7e-bda05dc0f1d1'></a>

In a store, for a given category, there may be two realizations of an assortment change :
1. When one or more items are dropped from the assortment, customers who intended to buy any of the dropped items, might either choose to opt for another 'substitutable' item or walk away from the store, without a purchase.

<a id='b682244a-9d2f-4d21-bb75-78b96ae69326'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='9d53fb78-fd5e-43ba-9a23-ec8e96487924'></a>

2. When one or more items are introduced into the assortment, customers who purchased any of the new items, might either buy the new item out of impulse or replace purchasing an existing item with the new item.

<a id='6dda45e1-92d1-4dfb-989a-3fdfaab52933'></a>

A better understanding of this underlying process would help in identifying the optimum assortment for the particular category in the particular store. In this paper, we aim to model the mechanism of demand transference so as to optimize the store assortment, for the category.

<a id='32fef5e4-ba2f-4227-b51c-c2ffd0f3889e'></a>

## 2. LITERATURE REVIEW
This section briefly discusses about the studies in place related to assortment selection / optimization.

<a id='1d027c0b-b61a-4b05-a04b-fd7e909b00ca'></a>

The common points among the available literatures is that they all look to optimize the assortment, based on maximizing cost function (usually sales or profit). We here would only restrict ourselves towards those studies which deal with the item attributes along with the scanner data.

<a id='5dd64000-865a-4ebe-b6a1-517a1b3dc526'></a>

Among the available articles, Fisher and Vaidyanathan (Fisher et al., 2009) look into selecting the optimum number of items from the available lot, to maximize sales. They have defined an approach, in which they view a item as a set of attribute values, use sales history of the items currently carried by the retailer to estimate the demand for each of the attribute values and from this, the demand for any potential item currently not carried by the retailer. They also introduce a model of substitution behavior, estimate the parameters and consider the impact of substitution in choosing assortment.

<a id='17d3d103-9b2e-4dd9-92cd-18609e918dca'></a>

Kök and Fisher (2007), also tread similar lines wherein they study an assortment planning model in which consumers might accept substitutes when their favorite product is unavailable. They develop an algorithmic process to help retailers compute the best assortment for each store, by estimating the parameters of substitution behavior and demand for products at a store, including products that have not been carried previously in that store. Finally, they propose an iterative optimization heuristic to solve the assortment planning problem.

<a id='883135fe-66bf-49a1-a372-753c80920b61'></a>

Other articles like Rooderkerk et al., (2013) look into price optimization along with promotion and shelf space optimization. Herein, they adopt a scalable assortment optimization method that allow for theory based substitution patterns and cross marketing mix effects. For the optimization part, they propose a large neighborhood search heuristic methodology.

<a id='dcfd7f01-694a-439c-91f9-8b9a334250e4'></a>

Our study though on similar lines, addresses an entirely different aspect of assortment study. This is more of scenario based, to understand how the store assortment performs when a change in the store assortment is realized. Basically, we help the retailer to decide which items to drop from the assortment, by helping him understand where the demand of the deleted item would flow to and in what magnitude. The retailer also gets a glimpse of additional incremental demand as well as the magnitude and direction of cannibalization that might be realized when additional items are added to the assortment. In the process of obtaining these insights, he also gets an understanding as to how the items in the new assortment will perform in the future.

<a id='49926155-ce5f-47e5-9924-2313ab967d70'></a>

### 3. METHODOLOGY
Demand is a latent feature, which can be experienced but not explicitly observed. Thus, modeling of demand and validation of the same becomes difficult. The nearest proxy to demand is sales. So, here we try to model the sales of each of the products offered in an assortment.

<a id='522cbd11-415b-4bdb-89d6-e7a6ee04b90a'></a>

Our methodology consists of a sales model, described in section 3.1 and a predictive algorithm based on the sales model, as described in section 3.2.

<a id='a8a94b84-69df-489b-ad65-7bf003c4faa1'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='eb58a6f2-32a7-4fdf-9065-cde59bf18658'></a>

### 3.1. Sales model

Before formulating the model, we look at a significant challenge encountered while developing the sales model: modeling store level UPC sales on attributes. UPC (Universal Product Code) is used to identify trade items in stores across different retailers and markets. UPC is aggregation of items which can vary across different regions.

<a id='d8e28680-586d-440e-99d8-243462f1e60e'></a>

### 3.1.1. Modeling framework
To model UPC sales at a store level, we chose store-level scanner data, as it provides a holistic view of the available assortment in the store. An example of the input data is provided in Table 1 under section 4.1. Our approach of modeling UPC sales on UPC attributes is motivated by the assertion that customers do not form preference of each individual UPC in a product category but that these preferences are derived from the preferences for the underlying attributes (e.g., size, brand, flavor, etc.). Theoretical justification of the same is available in economics (Lancaster, 1971) and psychology (Fishbein, 1967).

<a id='e98af05a-f4ec-4cce-b71b-825667713e6c'></a>

Our model thus takes into account the UPC attributes, in order to model UPC sales. Apart from the UPCs own attributes, attributes of other available UPCs would also affect the sales. We thus incorporate variables to account for a UPCs attribute similarity as well as cross attribute similarity with the other UPCs in the assortment.

<a id='6b83598e-c183-40f7-a465-109eb4baa740'></a>

### 3.1.2. Modeling formulation
We would now develop the attribute based model and highlight the role similarity variables play. While modeling UPC sales at a store level, we allow for flexible substitution patterns, and non-linear effects by starting with a log-log model (Rooderkerk et al., 2013), similar to the SCAN*PRO model (Wittink et al., 1988):

log($S_{kti}$) = $\underbrace{\alpha_{ki}}_{A}$ + $\underbrace{\beta.log(P_{kti})}_{B}$ + $\underbrace{\sum_{m \in A} \gamma_{kmti}}_{C}$ (1)

<a id='5fbee7d1-c73c-4274-9ae0-73e136febe81'></a>

where,

$S_{kti}$ = unit sales of UPC $k \in \{1, 2, ..., K\}$ in week $t \in \{1, 2, ..., T\}$ in store $i \in \{1, 2, ..., n\}$;

$\alpha_{ki}$ = UPC-store intercept for UPC $k \in \{1, 2, ..., K\}$ in store $i \in \{1, 2, ..., n\}$;

$P_{kti}$ = price of UPC $k \in \{1, 2, ..., K\}$ in week $t \in \{1, 2, ..., T\}$ in store $i \in \{1, 2, ..., n\}$;

$\gamma_{kmti}$ = similarity score of UPC $k \in \{1, 2, ..., K\}$, for attribute $m \in \mathcal{A}$, in week $t \in \{1, 2, ..., T\}$ in store $i \in \{1, 2, ..., n\}$;

$\mathcal{A}$ = set of all attributes, evaluated for all UPCs in a product category;

<a id='e4be5fb4-90e5-4d1e-8d3f-9eb4783bf75a'></a>

Further, $\alpha_{ki}$ may be replaced by strictly store level intercepts along with attribute dummies such that

$\alpha_{ki} = \underbrace{\alpha_i}_{A} + \underbrace{\sum_{m \in A} \sum_{l=1}^{m_l} A_{kml}}_{B}$ (2)

<a id='22d51e16-37b9-413a-a503-a1c0dec6eb91'></a>

where,

&nbsp;&nbsp;&nbsp;&nbsp;A_kml = 1 if UPC k possesses level l of attribute m ∈ A, and 0 otherwise, if m is nominal

&nbsp;&nbsp;&nbsp;&nbsp;A_kml = the realization of attribute m ∈ A, if m is metric

<a id='2ac3f0e3-f814-4e4c-8917-c1749deece1a'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='81080a06-ccf7-4c69-ac92-83d9bfea0963'></a>

### 3.1.3. Attribute similarity score
The similarity score of UPC _k_, for a nominal or metric attribute _m_, in week _t_, in store _i_ is defined such that it varies between 0 (minimum similarity) and 1 (maximum similarity), and also reflects the similarity of UPC _k_ relative to the distribution of attribute _m_ in the entire available assortment.

<a id='140bf983-6e09-4607-821e-5043a13872b4'></a>

Let $SIM_{kk'mti}$ denote the magnitude of similarity between UPC $k$ and UPC $k'$ with respect to attribute $m$ in store $i$ in week $t$.

<a id='c077f048-44cd-40b2-b7ab-73e2b73e2782'></a>

Further to the above discussed features of similarity, if UPC k and UPC k' share the same level of nominal attribute m, then the perceived similarity of UPC k and UPC k' should be stronger when their shared attribute level occurs less frequently (Goodall, 1966). We obtain all the above, by defining :

<a id='411e33cb-364e-4ce0-a397-be880b3dc101'></a>

$$SIM_{kk'mti} = I\{A_{k'm} = A_{km}\}. \left(1 - \frac{1}{N_{ti}} \sum_{k''=1, x_{k''ti}=1}^{K} I\{A_{k''m} = A_{km}\} \right) \quad (3a)$$

<a id='140d957e-5bf5-41eb-9713-b3d043cc9803'></a>

if attribute _m_ is nominal, where,

I{·} = an indicator function which takes the value 1 if its argument holds, 0 otherwise;

_A_<sub>_km_</sub> = the level attained by UPC _k_ on attribute _m_ such that _A_<sub>_km_</sub> = _l_ ⇔ _A_<sub>_kml_</sub> = 1;

_N_<sub>_ti_</sub> = the number of UPCs present in week _t_ in store _i_;

_x_<sub>_kti_</sub> = 1, if UPC _k_ was available in store _i_, for at least 1 day in week _t_; else 0.

<a id='fc1d315e-e487-4fba-b564-6be0d6659b22'></a>

Table 3 in section 4.2 illustrates how this would work for a Brand attribute.

<a id='b2684216-450a-4e8e-8e87-c1fa42f269ed'></a>

On the other hand, the similarity of UPC k and UPC k', with respect to a metric attribute m, is perceived to be more if there exists fewer UPCs with attribute values between the attribute values of UPC k and UPC k'. This is obtained by defining:

<a id='a047fbf7-267f-4d68-8c5f-cd3abacd15ac'></a>

$$SIM_{kk'mti} = 1 - \frac{1}{N_{ti}} \cdot \sum_{\substack{k''=1 \\ x_{k''ti}=1}}^{K} I\{\min(A_{km}, A_{k'm}) \leq A_{k''m} \leq \max(A_{km}, A_{k'm})\} \quad (3b)$$

<a id='7bc790e6-4f5c-4aaa-9e52-90f8db4fd477'></a>

if attribute _m_ is metric.
This definition is numerically illustrated for Weight attribute in Table 5 in section 4.2.

<a id='d04dacb5-373d-4965-b180-e598b1a268a0'></a>

Once we have described the measure of similarity for UPC k and UPC k', we may now formulate the similarity score of UPC k for attribute m in week t in store i as:

$\gamma_{kmti} = mean^*_{k'\neq k} (SIM_{kk'mti})$

(4)

<a id='77d12cdc-f455-4b63-b5c6-ceb3b6f13b0a'></a>

where,
$mean^*(.) = \text{Arithmetic Mean of the non-zero elements of the argument, if attribute } m \text{ is}$
nominal, usual Arithmetic Mean otherwise.

<a id='7375e443-aba1-481f-8d2f-58be7de403d3'></a>

### 3.1.4. Model implementation
The model described in this paper, is best implemented when modeled category wise. Now, each category has properties of its own and consists of widely different varieties of UPCs. The two major category properties that is observed is as follows:

<a id='24a89b50-1f3a-424b-bea0-5c0a3ea14f0e'></a>

1. Demand might get transferred to any and every UPC of the category and

<a id='085c3047-6c14-4beb-b2c5-0ae10d66c54c'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753
Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='76d16279-988b-4674-9f44-f590ca1a3cb2'></a>

2. Transfer of demand is restricted only within mutually exclusive and exhaustive set of substitutable groups, which are very different from each other (further discussed in section 4.3).

<a id='fc138661-d3e0-4fcf-a43a-ce25535090d3'></a>

For case 2, one may carry on the same analysis over each substitutable group, as if assuming it to be a small sized category of sorts.

<a id='44170b47-e074-403d-8b16-1c423ec7bbef'></a>

Since we have formulated a linear regression as mentioned in (1), all regression sanity checks have been taken care of and the final model thus only consists of the uncorrelated and significant regressors among the ones mentioned in (1).

<a id='28f8921d-c5a3-4a65-86d6-b134da1ccf77'></a>

## 3.2. Predictive algorithm
We would now look into how to predict the magnitude of demand transference and the walkoff rate.
Define

<a id='28e996e2-24b4-49b0-808f-eb7d90896da4'></a>

A_i : the training assortment of store i;
A'_i : the assortment of store i after the assortment change;

<a id='b4c5ecb9-1b73-43ec-b04b-c5965a008257'></a>

Now, for every UPC in A_t, we can easily obtain the predicted weekly unit sales from the model as explained in (1).

<a id='7b381c9b-169a-41da-b819-0df282b84ce5'></a>

Also, the values of parts A and B in (1) are independent of the store assortment (assuming there is no change in price in any of the items in Aᵢ) and thus doesn't change. It suffices to compute these values only for those UPCs that have been introduced in A'ᵢ but were not a part of Aᵢ. Part C in (1) directly depends upon the current assortment in store and hence the similarity score is recalculated for each UPC in the new assortment. Once we have all the required information, the predicted weekly unit sales of every UPC in Aᵢ can be easily obtained.

<a id='323b1f5a-2afe-42ed-9662-fe53d176cda8'></a>

Define,

$\hat{S}_{ki}$ = predicted weekly unit sales of UPC $k \in A_i$;

$\hat{S}'_{ki}$ = predicted weekly unit sales of UPC $k \in A'_i$;

<a id='59cce42c-d5f6-4baf-8186-9040d9af5f52'></a>

Therefore,

<a id='778deeeb-13d6-4dca-bb71-d8fdd41f62ea'></a>

$\Delta S_{ki} = \hat{S}'_{ki} - \hat{S}_{ki}$, is the change in the weekly unit sales of UPC $k \in A_i \cap A'_i$.
But, $\Delta S_{ki} = \hat{S}'_{ki}$, if UPC $k \in A'_i \setminus A_i$

<a id='dcb838ad-153f-4130-89ec-e31f00b9adcd'></a>

### 3.2.1. Case of item deletion
Define $U_{del}$ = set of UPCs that have been deleted from $A_i$, and are not present in $A'_i$. Then,

<a id='d67cd7c1-3ecf-4090-b46c-e6e3976ecee7'></a>

$\Delta_{kA'i}^{del} = \frac{\Delta S_{ki}}{\sum_{t \in u_{del}} \hat{S}_{ti}} . 100 \%$ (5a)

<a id='ba945b3e-7181-4083-a6d8-191dbaaeba17'></a>

where,

<a id='2456c0e0-f186-4cc6-949e-1cfb364b4a92'></a>

$\Delta_{kA'_i}^{del}$ = demand of UPCs in $U_{del}$ transferred to UPC $k$, $\forall k \in A'_i$.

<a id='ccb02a59-81db-40af-97ed-8ad5007113b9'></a>

Herein, the walk-off rate is calculated as:
$ω_{A'_i}^{del} = 100 - \sum_{k \in A'_i} Δ_{kA'_i}^{del}$ (5b)

<a id='ee565188-c967-4145-8816-bc3595072c82'></a>

### 3.2.2. Case of item addition
Define, U_add = set of UPCs that have been added to A'_i, but were not a part of A_i. Then,

<a id='a5abfcf3-90aa-452a-af13-5b2c881ce419'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='9846de16-f073-481d-8bb0-de8bc65dae47'></a>

$$\Delta_{k A'_i}^{add} = \frac{|\Delta S_{ki}|}{\sum_{t \in u_{add}} \hat{S}_{ti}'} \cdot 100 \%$$ (6a)

<a id='cf384835-b635-4294-bf33-9df4e5b1dcf4'></a>

where,

<a id='5bfbe30e-dfba-41a2-83e5-4689e765ea7f'></a>

$\Delta_{kA'_i}^{add} = \text{demand of UPCs in } U_{add} \text{ cannibalized from UPC } k, \forall k \in A'_i.$

<a id='a5102bf4-7a66-4457-bfec-1a1a05164524'></a>

Herein, the incrementality is calculated as:

$$\omega_{A'_i}^{add} = 100 - \sum_{k \in A'_i} \Delta_{kA'_i}^{add} \quad (6b)$$

<a id='84734d48-6802-4fee-b763-67321de27bab'></a>

### 3.2.3. Case of both item deletion and item addition
In this case, it becomes difficult to identify separately, what amount of the change in the demand for UPC _k_, is due to the transfer of demand from the deleted UPCs and how much amount is due to cannibalization of the added UPCs. Further, there could even be some amount of demand transference towards the newly added UPCs as well.

<a id='44b18853-8448-4aea-a412-e727a0a4b31f'></a>

Hence, one may separately consider the deletions and additions to obtain the demand transference measures.

<a id='d28e8963-8b1b-4369-9078-ac0cfb9e468c'></a>

Therefore, we have

<a id='f0d22e1f-e416-457c-a550-2b4353b9ea88'></a>

$$\Delta_{K A'_i}^{add} = \frac{|\Delta S_{ki}| \cdot |\mathcal{U}_{add}|}{|\mathcal{U}_{del}| \cdot \sum_{t \in \mathcal{U}_{add}} \hat{S}_{ti}} \cdot 100 \%, \forall k \in A'_i \quad (7a)$$

<a id='f94c1801-7633-4da0-9e90-33f57abdf975'></a>

$$\Delta_{kA'i}^{del} = \frac{\Delta S_{ki} \cdot \frac{|U_{del}|}{|U_{add}|}}{\sum_{t \in U_{del}} \hat{S}_{ti}} \cdot 100\%, \quad \forall k \in A'_i \quad (7b)$$

<a id='69c1edd2-89f9-4b05-a8ee-8d2da04174e2'></a>

where,

$\Delta_{kA'_i}^{add}$ = demand of UPCs in $U_{add}$ cannibalized from UPC $k$, $\forall k \in A'_i$.

$\Delta_{kA'_i}^{del}$ = demand of UPCs in $U_{del}$ transferred to UPC $k$, $\forall k \in A'_i$.

<a id='7e410f03-9369-431b-ace6-1606c264827c'></a>

In (7b),

$ΔS_{ki} = ΔS_{ki} · (1 - \sum_{t∈\mathcal{U}_{add}} \frac{Δ_{tA^i}^{add}}{100} · I\{k ∈ \mathcal{U}_{add}\})$ (7c)

<a id='904ee41f-4f20-47e0-949d-5c07e7827827'></a>

Therefore, walkoff rate is:

$\omega_{A'_i}^{del} = 100 - \sum_{k \in A'_i} \Delta_{kA'_i}^{del}$

(7d)

<a id='cb7d7641-59c0-4616-abe4-3cc2611860f0'></a>

and incrementality is defined as:

<a id='0b978a7a-1a3d-41a2-a713-5452a094b0fb'></a>

$$\omega_{A'_i}^{add} = 100 - \sum_{k \in A'_i} \Delta_{kA'_i}^{add} - \sum_{k \in \mathcal{U}_{add}} \Delta_{kA'_i}^{del} \quad (7e)$$

<a id='f62e354f-dbab-44b1-a602-c83c4b71db6a'></a>

4. DISCUSSION

<a id='5ebaa413-3731-4ea4-818e-81c277d7f96e'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753
Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='264d88e7-473b-4570-92d8-f489e1c29fed'></a>

Here, we will have a brief walkthrough of a sample input data for the algorithm along with the similarity calculation for the same.

<a id='09261fdc-95eb-4a94-ab3a-ef57b127dab0'></a>

## 4.1. Scanner data and attribute data
Table 1 refers to a snapshot of the scanner data that we require to carry on with the analysis.
The snapshot here has been restricted to 4 UPCs, in 3 weeks and 1 store.

<a id='5179b3fe-ac67-4ef1-a682-223f1b87446e'></a>

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

<a id='fcf01c57-1fdc-425b-86a0-5d7edb57a46c'></a>

Table 2 Attribute information for UPCs in the snapshot
<table id="7-1v">
<tr><td id="7-1w">UPC</td><td id="7-1x">Brand</td><td id="7-1y">Weight (in gm)</td></tr>
<tr><td id="7-1z">UPC 1</td><td id="7-1A">Brand 1</td><td id="7-1B">200</td></tr>
<tr><td id="7-1C">UPC 2</td><td id="7-1D">Brand 1</td><td id="7-1E">180</td></tr>
<tr><td id="7-1F">UPC 3</td><td id="7-1G">Brand 1</td><td id="7-1H">200</td></tr>
<tr><td id="7-1I">UPC 4</td><td id="7-1J">Brand 2</td><td id="7-1K">150</td></tr>
</table>

<a id='8c135c78-d3f4-4157-becf-02096b2327fe'></a>

**4.2. Computing the attribute similarity score**
As depicted in Table 2, there are two attributes to take care of viz. Brand (a nominal attribute) and Weight (a metric attribute).

<a id='10388963-bce2-47cb-8ffc-8d77c2e508b3'></a>

For attribute Brand, Brand 1 is present in 75% of the overall assortment, whereas Brand 2 is present in 25% of the overall assortment.

<a id='a7577216-962b-4912-bb07-bdb0cb3cd852'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='37a7b3d5-44d9-4439-8bdb-d1bc1b58e48c'></a>

Hence, according to this example, the similarity scores for UPC 1 with respect to the nominal attribute Brand is demonstrated in Table 3 below:

<a id='9eb9d385-bfd6-41c5-8316-ed3533e3042d'></a>

Table 3 Week wise brand similarity score for UPC 1
<table id="8-1">
<tr><td id="8-2">Week No.</td><td id="8-3">Brand 1 presence</td><td id="8-4">Brand similarity score (γkmti)</td></tr>
<tr><td id="8-5">1</td><td id="8-6">66.67%</td><td id="8-7">0.33</td></tr>
<tr><td id="8-8">2</td><td id="8-9">75.00%</td><td id="8-a">0.25</td></tr>
<tr><td id="8-b">3</td><td id="8-c">75.00%</td><td id="8-d">0.25</td></tr>
</table>

<a id='6f3c43a7-1580-42b0-9ec8-75e1543933fe'></a>

Similarly, for the metric attribute Weight, similarity score of UPC 1 is seen to be as described in Table 5 below:

<a id='5aca5850-a412-4406-a7e1-209c2b2c106c'></a>

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

<a id='1e8ab8e5-3c08-44ac-b17a-185b23f85a38'></a>

Therefore,
<table id="8-T">
<tr><td id="8-U" colspan="2">Table 5 Weekly weight similarity score for UPC 1</td></tr>
<tr><td id="8-V">Week No.</td><td id="8-W">Weight Similarity score</td></tr>
<tr><td id="8-X">1</td><td id="8-Y">0.165</td></tr>
<tr><td id="8-Z">2</td><td id="8-10">0.250</td></tr>
<tr><td id="8-11">3</td><td id="8-12">0.250</td></tr>
</table>

<a id='ec96b7b9-1463-4efa-b83f-396712714763'></a>

### 4.3. Substitutable groups
A category can be divided into mutually exclusive and exhaustive groups of items, called substitutable groups. A substitutable group consists of items that are more likely to be substitutes of each other, than that of items in the other substitutable groups.

<a id='ddeaf454-8156-4da6-9f38-5fdc8baaa641'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='72f81b25-3390-45bf-8e1b-eb7690f3bc16'></a>

We accomplish this segmentation into substitutable group by using a proprietary graph partition based algorithm.

<a id='456f1581-6ac9-4b19-b1d3-e8f56b4ae5e9'></a>

When, implemented for a substitutable group, the demand transfer algorithm restricts the transfer of demand within the same group; since by definition, there is very less probability of items in other groups to be proper substitutes.

<a id='f693605f-e7ba-437e-a504-61ab6fdb0f18'></a>

## 4.4. Parallelization techniques
The entire algorithm was executed in R, for a category with 7 substitutable groups, available in 4500 stores.

<a id='b5ea001c-2a96-4d15-87d3-46b219bbc1de'></a>

While *Hadoop streaming* was used to execute the algorithm over stores; for a store, the *mclapply* function (which uses forking technique) from *parallel* package was used to parallelize over substitutable groups.

<a id='e9305495-257f-48bf-be0b-a61674f84b26'></a>

For a fixed store, the runtime in R (using forking via _mclapply_) is comparable to the runtime when executed in Python without any scaling up technique.

<a id='d778a014-5be2-466a-8dda-9515aed2e76f'></a>

## 4.5. Results and success stories
This algorithm has been run for a variety of categories, both General Merchandise and Fast-Moving Consumer Goods (like Yogurt, Light Bulbs, Dish Soap, Utility Pants, Food Storage, etc.) and has been seen to be performing really well.

<a id='fb3cb946-daa4-4ea8-8672-7dcff3b3107b'></a>

The Mean Absolute Percentage Error for the model, when validated against observed assortment changes for the aforementioned categories, was almost always in the range of 4% to 13%.

<a id='453bd19c-af34-444a-b261-112625996f4e'></a>

## 5. CONCLUSION
The problem of demand transference is an important one for any retailer. Obviously, the retailer cannot keep on carrying the same assortment over time. Market trends as well as the item performance, will always compel him to offer his customers the best assortment so as to maximize sales and customer satisfaction. Hence, it is better off to know from beforehand the magnitude of demand transference or cannibalization, that might be experienced with regards to a particular change in his assortment. Having a good understanding of the different scenarios will surely let him plan better than his competitors, and establish his stand in the market.

<a id='9fcf2b50-5468-4f74-8831-1cef255f214e'></a>

Wrong choice of item deletion, might have severe repercussions in the form of:
1. churning of customer base which were loyal to the deleted product; or
2. churning of customer base, due to unavailability of proper substitutes of the deleted product in the available assortment.

<a id='a49045cb-c42b-46e1-a4a4-d4d699ce0fdf'></a>

Similarly, wrong choice of item addition could also be detrimental in the form of the new item not attracting any incremental demand of its own, but is only cannibalizing the demand of the other available items in the assortment, thus not doing any significant good to the retailer.

<a id='3ccd2d8e-56bf-4aa9-8e83-4f910d594f68'></a>

This study has been aimed to help the retailer address these basic problems of assortment.

<a id='daa190f9-3d17-4926-ba37-98a06b64297c'></a>

## 6. REFERENCES
Fishbein M, ed. (1967) *Attitude and Prediction of Behavior* (John Wiley & Sons, New York).
Fisher ML, Vaidyanathan R (2009) An Algorithm and Demand Estimation Procedure for Retail Assortment Optimization. The Wharton School, Philadelphia, Pennsylvania.
Goodall DW (1966) A new similarity index based on probability. *Biometrics* 22(4):882–907.

<a id='eecc6acf-30b1-4964-8edf-441dea6da722'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='b99aa229-9664-419c-8f82-324b92ee78cd'></a>

Kök, G., M. L. Fisher. 2007. Demand Estimation and Assortment Optimization under
Substitution: Methodology and Application. Operations Research 55(6) 1001–1021.
Lancaster K (1971) Consumer Demand: A New Approach (Columbia University Press, New
York).

<a id='74277bf9-1358-49b3-9a1c-dd692c9a5a85'></a>

Rooderkerk RP, van Heerde HJ, Bijmolt TH (2011) Optimizing Retail Assortments. *Marketing Science* 32(5):699–715.

<a id='aedc941a-d60e-405f-8296-a43b29835c10'></a>

Wittink DR, Addona MJ, Hawkes W, Porter JC (1988) SCAN*PRO:The estimation, validation, and use of promotional effects based on scanner data. Working paper, Cornell University, Ithaca, NY.

<a id='fa7b853f-2826-4d2c-9612-5a75bae382fa'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753