<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class ThumborController extends AbstractController
{
    /**
     * @Route("/thumbor_demo", name="thumbor_demo")
     */
    public function demo(): Response
    {
        return $this->render('thumbor/index.html.twig');
    }
}
