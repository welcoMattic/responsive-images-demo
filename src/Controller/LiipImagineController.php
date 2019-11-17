<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;

class LiipImagineController extends AbstractController
{
    /**
     * @Route("/liip/imagine", name="liip_imagine")
     */
    public function index()
    {
        return $this->render('liip_imagine/index.html.twig', [
            'controller_name' => 'LiipImagineController',
        ]);
    }
}
